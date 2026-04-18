import os
import shutil
import json
from pathlib import Path

# Configuration
ROOT_DIR = Path(".")
TARGET_DIR = ROOT_DIR / "consolidated_curriculum"
ANALYSIS_FILE = "structure_analysis.json"

# Topic Standardization Map
TOPIC_RENAME = {
    "01-intro": "01-intro-to-ds",
    "02-python-sql": "02-python-sql",
    "03-pandas": "03-pandas-eda",
    "04-eda-visualization": "03-pandas-eda",  # merge into pandas/eda
    "05-knn-classification": "04-knn-classification",
    "06-linear-regression": "05-linear-regression",
    "07-regularization": "05-linear-regression",  # merge into linear regression
    "08-logistic-regression": "06-logistic-regression",
    "09-model-evaluation": "07-model-evaluation",
    "10-decision-trees": "08-decision-trees-forests",
    "11-nlp": "09-nlp-naive-bayes",
    "12-clustering": "10-clustering",
    "13-dimensionality-reduction": "11-dimensionality-reduction",
    "14-recommender-systems": "12-recommender-systems",
    "15-time-series": "13-time-series",
    "16-neural-networks": "14-neural-networks",
    "17-big-data": "15-big-data-cloud",
    "18-web-scraping": "16-web-scraping",
    "19-projects": "17-projects-case-studies"
}

def main():
    if TARGET_DIR.exists():
        shutil.rmtree(TARGET_DIR)
    TARGET_DIR.mkdir()

    with open(ANALYSIS_FILE, 'r') as f:
        analysis_data = json.load(f)

    print("Starting consolidation based on structure_analysis.json...")

    path_to_topic = {}
    for old_topic, paths in analysis_data.items():
        new_topic = TOPIC_RENAME.get(old_topic, old_topic)
        for path_str in paths:
            if path_str.startswith("./"):
                path_str = path_str[2:]
            path_to_topic[path_str] = new_topic

    # Filter out child paths already covered by a parent in the same topic
    sorted_paths = sorted(path_to_topic.items(), key=lambda x: len(Path(x[0]).parts))
    filtered_paths = {}
    for path_str, topic in sorted_paths:
        path = Path(path_str)
        is_child = any(
            str(parent) in filtered_paths and filtered_paths[str(parent)] == topic
            for parent in path.parents
        )
        if not is_child:
            filtered_paths[path_str] = topic

    # Group by topic
    topic_groups = {}
    for path_str, topic in filtered_paths.items():
        src_path = Path(path_str)
        if not src_path.exists():
            print(f"  [SKIP] Missing path: {path_str}")
            continue
        topic_groups.setdefault(topic, []).append((src_path.parts[0], src_path))

    promotion_log = {}

    for topic, items in sorted(topic_groups.items()):
        print(f"\nProcessing {topic} ({len(items)} sources)...")
        topic_dir = TARGET_DIR / topic
        variations_dir = topic_dir / "variations"
        reference_dir = topic_dir / "reference"
        topic_dir.mkdir(parents=True, exist_ok=True)
        variations_dir.mkdir(exist_ok=True)
        reference_dir.mkdir(exist_ok=True)

        best_score = -1
        best_candidate = None

        for repo_name, src_path in items:
            base_name = f"{repo_name}_{src_path.name}"
            dest_path = variations_dir / base_name
            # Handle collisions by appending a counter
            counter = 1
            while dest_path.exists():
                dest_path = variations_dir / f"{base_name}_{counter}"
                counter += 1

            try:
                if src_path.is_dir():
                    shutil.copytree(src_path, dest_path,
                                    ignore=shutil.ignore_patterns('.git', '.ipynb_checkpoints', '__pycache__'))
                else:
                    continue

                # Copy PDFs to reference
                for pdf in dest_path.rglob("*.pdf"):
                    shutil.copy2(pdf, reference_dir / f"{repo_name}_{pdf.name}")

                # Score this candidate
                score = 0
                if "DAT-23-NYC" in repo_name: score += 100
                if "DAT-NYC-37" in repo_name: score += 50
                if "lesson" in src_path.name.lower(): score += 10
                notebooks = list(dest_path.rglob("*.ipynb"))
                if notebooks:
                    score += len(notebooks)
                    score += max(nb.stat().st_size for nb in notebooks) / 1_000_000

                print(f"  {repo_name}/{src_path.name}  score={score:.1f}")

                if score > best_score:
                    best_score = score
                    best_candidate = (dest_path, repo_name, src_path)

            except Exception as e:
                print(f"  [ERROR] {src_path}: {e}")

        # Promote best candidate's contents into topic_dir
        if best_candidate:
            dest_path, repo_name, src_path = best_candidate
            print(f"  => Promoting {repo_name}/{src_path.name} (score={best_score:.1f})")
            promotion_log[topic] = f"{repo_name}/{src_path}"
            for item in list(dest_path.iterdir()):
                target = topic_dir / item.name
                if not target.exists():
                    shutil.move(str(item), str(target))
            shutil.rmtree(dest_path)  # remove now-empty or residual dir

    # Write promotion log
    log_path = TARGET_DIR / "promotion_log.json"
    with open(log_path, 'w') as f:
        json.dump(promotion_log, f, indent=4)
    print(f"\nConsolidation complete. Promotion log: {log_path}")

if __name__ == "__main__":
    main()
