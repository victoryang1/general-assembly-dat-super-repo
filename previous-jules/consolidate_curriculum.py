import os
import shutil
import json
from pathlib import Path

# Configuration
ROOT_DIR = Path(".")
TARGET_DIR = ROOT_DIR / "consolidated_curriculum"
ANALYSIS_FILE = "structure_analysis.json"

# Topic Standardization Map
# The analysis script produced topics like "01-intro".
# I want to map them to my final refined taxonomy if they differ.
# Or just use the analysis topics if they are good enough.
# Let's refine them here.
TOPIC_RENAME = {
    "01-intro": "01-intro-to-ds",
    "02-python-sql": "02-python-sql",
    "03-pandas": "03-pandas-eda",
    "05-knn-classification": "04-knn-classification",
    "06-linear-regression": "05-linear-regression",
    "07-regularization": "05-linear-regression", # Merge into Linear Regression
    "08-logistic-regression": "06-logistic-regression",
    "10-decision-trees": "07-decision-trees-forests",
    "11-nlp": "08-nlp-naive-bayes",
    "12-clustering": "09-clustering",
    "13-dimensionality-reduction": "10-dimensionality-reduction",
    "14-recommender-systems": "11-recommender-systems",
    "15-time-series": "12-time-series",
    "16-neural-networks": "13-neural-networks",
    "17-big-data": "14-big-data-cloud",
    "18-web-scraping": "15-web-scraping", # New topic I missed in taxonomy, let's keep it
    "19-projects": "16-projects-case-studies"
}

def main():
    if TARGET_DIR.exists():
        shutil.rmtree(TARGET_DIR)
    TARGET_DIR.mkdir()
    
    # Load analysis
    with open(ANALYSIS_FILE, 'r') as f:
        analysis_data = json.load(f)
        
    print("Starting consolidation based on structure_analysis.json...")
    
    # Invert the map: Path -> Topic
    # And handle renames
    path_to_topic = {}
    
    for old_topic, paths in analysis_data.items():
        new_topic = TOPIC_RENAME.get(old_topic, old_topic)
        for path_str in paths:
            # path_str is like "./DAT-NYC-37/lessons"
            # Normalize path
            if path_str.startswith("./"):
                path_str = path_str[2:]
            path_to_topic[path_str] = new_topic

    # Identify distinct valid source paths
    # The analysis might have included nested paths.
    # We prefer to move the largest containing folder if possible.
    # Filter out paths that are children of other paths in the same topic
    
    # Sort paths by length so parents come first (shorter path)
    sorted_paths = sorted(path_to_topic.items(), key=lambda x: len(Path(x[0]).parts))
    
    filtered_paths = {}
    
    for path_str, topic in sorted_paths:
        path = Path(path_str)
        # Check if any parent of this path is already mapped to the SAME topic
        is_child = False
        for parent in path.parents:
            parent_str = str(parent)
            if parent_str in filtered_paths and filtered_paths[parent_str] == topic:
                is_child = True
                break
        
        if not is_child:
            filtered_paths[path_str] = topic

    # Group by Topic
    topic_groups = {} # Topic -> List of (RepoName, SourcePath)
    
    for path_str, topic in filtered_paths.items():
        src_path = Path(path_str)
        if not src_path.exists():
            print(f"Skipping missing path: {path_str}")
            continue
            
        if topic not in topic_groups:
            topic_groups[topic] = []
            
        # Extract Repo Name
        parts = src_path.parts
        repo_name = parts[0] if len(parts) > 0 else "unknown"
        
        topic_groups[topic].append((repo_name, src_path))
        
    # Process each topic
    for topic, items in topic_groups.items():
        print(f"Processing {topic}...")
        topic_dir = TARGET_DIR / topic
        variations_dir = topic_dir / "variations"
        reference_dir = topic_dir / "reference"
        
        topic_dir.mkdir(parents=True, exist_ok=True)
        variations_dir.mkdir(exist_ok=True)
        reference_dir.mkdir(exist_ok=True)
        
        candidates = []
        best_score = -1
        best_candidate = None
        
        for repo_name, src_path in items:
            # Destination name
            # sanitize src_path name to avoid slashes or weirdness if we just use name
            # If src_path is 'DAT-BOS-16/lessons/lesson-01', name is 'lesson-01'
            # We want 'DAT-BOS-16_lesson-01'
            dest_name = f"{repo_name}_{src_path.name}"
            dest_path = variations_dir / dest_name
            
            # Copy
            if dest_path.exists():
                # Append a number if collision
                dest_path = variations_dir / f"{dest_name}_dup"
            
            try:
                if src_path.is_dir():
                    shutil.copytree(src_path, dest_path, ignore=shutil.ignore_patterns('.git', '.ipynb_checkpoints', '__pycache__'))
                else:
                    # If it's a file? Analysis mainly returned dirs.
                    pass
                
                # Check for PDFs to copy to reference
                for pdf in dest_path.rglob("*.pdf"):
                     shutil.copy2(pdf, reference_dir / f"{repo_name}_{pdf.name}")

                # candidates.append(dest_path)
                
                # Determine "Score" for being the Main Lesson
                score = 0
                if "DAT-23-NYC" in repo_name: score += 100
                if "DAT-NYC-37" in repo_name: score += 50
                if "lesson" in src_path.name.lower(): score += 10
                
                # Check for notebook content
                notebooks = list(dest_path.glob("*.ipynb"))
                if notebooks:
                    score += len(notebooks)
                    # Check size of largest notebook
                    max_size = max(nb.stat().st_size for nb in notebooks)
                    score += max_size / 1000000 # Add points for MB size
                
                if score > best_score:
                    best_score = score
                    best_candidate = dest_path

            except Exception as e:
                print(f"Error copying {src_path}: {e}")

        # 3. Promote Best Candidate
        if best_candidate:
            print(f"  Promoting {best_candidate.name} to Main Lesson")
            # Move contents of best_candidate to topic_dir
            # We want to move the *contents* so the topic_dir becomes the lesson folder
            # But topic_dir already contains 'variations' and 'reference'.
            # So we move the files/folders from best_candidate to topic_dir
            
            for item in best_candidate.iterdir():
                target_item = topic_dir / item.name
                if target_item.exists():
                    # If collision (unlikely given we just created topic_dir, but 'variations' exists), skip or merge?
                    # 'variations' and 'reference' are already there.
                    # If the lesson has a folder named 'variations', we might have a problem. Unlikely.
                    # print(f"  Warning: Collision for {item.name} in {topic_dir}")
                    pass
                else:
                    shutil.move(str(item), str(target_item))
            
            # Remove the empty best_candidate folder from variations
            best_candidate.rmdir()

    print("Consolidation complete.")

if __name__ == "__main__":
    main()
