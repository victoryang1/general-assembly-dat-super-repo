import os
import json
import re

# Root directory is the current directory
ROOT_DIR = "."

# Known topics based on DAT-23-NYC (our "gold standard") and common DS curriculum
TOPICS = {
    "01-intro": ["intro", "setup", "git", "command line", "bash", "terminal"],
    "02-python-sql": ["python", "sql", "database", "sqlite", "postgres", "programming", "functions", "loops"],
    "03-pandas": ["pandas", "dataframe", "series", "matplotlib", "seaborn", "visualization", "plotting", "eda", "exploratory"],
    "04-eda-visualization": ["visualization", "plotting", "eda", "exploratory", "matplotlib", "seaborn"], # Overlap with pandas, might need refinement
    "05-knn-classification": ["knn", "k-nearest", "classification", "classifier", "neighbors"],
    "06-linear-regression": ["linear regression", "regression", "ols", "statsmodels", "scikit-learn"],
    "07-regularization": ["regularization", "lasso", "ridge", "elasticnet", "overfitting", "bias variance"],
    "08-logistic-regression": ["logistic regression", "logistic", "classification", "sigmoid", "logit"],
    "09-model-evaluation": ["evaluation", "metrics", "confusion matrix", "roc", "auc", "accuracy", "precision", "recall", "f1"],
    "10-decision-trees": ["decision tree", "random forest", "ensemble", "bagging", "boosting", "cart", "forest"],
    "11-nlp": ["nlp", "natural language", "text", "mining", "nltk", "spacy", "countvectorizer", "tfidf", "naive bayes"],
    "12-clustering": ["clustering", "kmeans", "dbscan", "hierarchical", "unsupervised"],
    "13-dimensionality-reduction": ["pca", "dimensionality reduction", "svd", "tsne", "manifold"],
    "14-recommender-systems": ["recommender", "recommendation", "collaborative filtering", "content based", "matrix factorization"],
    "15-time-series": ["time series", "arima", "forecasting", "temporal", "date time"],
    "16-neural-networks": ["neural network", "deep learning", "keras", "tensorflow", "pytorch", "mlp", "cnn", "rnn"],
    "17-big-data": ["big data", "spark", "hadoop", "mapreduce", "aws", "cloud"],
    "18-web-scraping": ["scraping", "beautifulsoup", "selenium", "scrapy", "api", "requests"],
    "19-projects": ["project", "capstone", "final"]
}

# Directories to ignore
IGNORE_DIRS = {".git", ".github", "consolidated_curriculum", "self_created_tools"}

def extract_text_from_ipynb(filepath):
    """Reads the first 5 markdown cells of a notebook to find keywords."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text_content = []
            cells = data.get('cells', [])
            count = 0
            for cell in cells:
                if cell.get('cell_type') == 'markdown':
                    text_content.append(" ".join(cell.get('source', [])))
                    count += 1
                    if count >= 5: # Limit to first 5 cells
                        break
            return " ".join(text_content).lower()
    except Exception as e:
        return ""

def guess_topic(directory):
    """Guesses the topic of a directory based on its name and contents."""
    dir_name = os.path.basename(directory).lower()
    
    # Check directory name first
    for topic_key, keywords in TOPICS.items():
        if any(kw in dir_name for kw in keywords):
            # Special case: 'python' often overlaps with 'intro' or 'pandas', be careful
            if "intro" in dir_name and topic_key == "01-intro": return topic_key
            if "pandas" in dir_name and topic_key == "03-pandas": return topic_key
            if "linear" in dir_name and topic_key == "06-linear-regression": return topic_key
            return topic_key

    # Scan contents
    content_text = ""
    # Look for README
    readme_path = os.path.join(directory, "README.md")
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                content_text += f.read(1000).lower() # Read first 1000 chars
        except:
            pass
            
    # Look for notebooks
    for file in os.listdir(directory):
        if file.endswith(".ipynb"):
            content_text += extract_text_from_ipynb(os.path.join(directory, file))
            if len(content_text) > 5000: # Limit text analysis
                break
                
    # Check content against keywords
    best_match = None
    max_score = 0
    
    for topic_key, keywords in TOPICS.items():
        score = sum(content_text.count(kw) for kw in keywords)
        if score > max_score:
            max_score = score
            best_match = topic_key
            
    return best_match

def analyze_repos():
    mapping = {}
    
    # Get all immediate subdirectories (the repositories)
    repos = [d for d in os.listdir(ROOT_DIR) if os.path.isdir(d) and d not in IGNORE_DIRS]
    
    for repo in repos:
        repo_path = os.path.join(ROOT_DIR, repo)
        print(f"Analyzing {repo}...")
        
        # Traverse the repo to find "lesson-like" directories
        for root, dirs, files in os.walk(repo_path):
            # Heuristic: verify if this folder contains lesson material (notebooks, pdfs)
            has_material = any(f.endswith(('.ipynb', '.pdf', '.md')) for f in files)
            if not has_material:
                continue

            # Skip deep nesting if parent is already mapped? 
            # Actually, sometimes lessons are nested. Let's just map leaf nodes or nodes with specific names.
            
            dir_name = os.path.basename(root).lower()
            
            # Skip likely non-lesson folders
            if dir_name in ['data', 'images', 'img', 'assets', 'static', '__pycache__', '.ipynb_checkpoints']:
                continue
                
            # Try to guess topic
            topic = guess_topic(root)
            
            if topic:
                if topic not in mapping:
                    mapping[topic] = []
                mapping[topic].append(root)
                # print(f"  Mapped {root} -> {topic}")
            else:
                # If no topic guessed, maybe mark as uncategorized
                pass

    with open("structure_analysis.json", "w") as f:
        json.dump(mapping, f, indent=4)
        
    print("Analysis complete. Saved to structure_analysis.json")

if __name__ == "__main__":
    analyze_repos()
