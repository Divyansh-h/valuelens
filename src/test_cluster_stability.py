import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.utils import resample
import yaml

from clustering import load_and_preprocess_rfm

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def test_stability():
    config = load_config()
    k = config['machine_learning']['k_clusters']
    
    print("Loading data for Bootstrap Stability Testing...")
    df, rfm_log = load_and_preprocess_rfm()
    
    print(f"Fitting base K-Means model (K={k}) on entire dataset...")
    base_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('kmeans', KMeans(n_clusters=k, random_state=42, n_init=10))
    ])
    
    base_pipeline.fit(rfm_log)
    base_labels = base_pipeline.predict(rfm_log)
    
    n_iterations = 20
    ari_scores = []
    
    print(f"Running {n_iterations} bootstrap iterations...")
    
    for i in range(n_iterations):
        # Sample with replacement
        bootstrap_sample = resample(rfm_log, replace=True, n_samples=len(rfm_log), random_state=i)
        
        # Fit new model on bootstrap sample
        boot_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=k, random_state=i, n_init=10))
        ])
        
        boot_pipeline.fit(bootstrap_sample)
        
        # Predict on the ORIGINAL dataset to compare against base labels
        boot_labels_on_full = boot_pipeline.predict(rfm_log)
        
        # Calculate ARI
        ari = adjusted_rand_score(base_labels, boot_labels_on_full)
        ari_scores.append(ari)
        print(f"Iteration {i+1:02d}/{n_iterations} | ARI: {ari:.4f}")
        
    mean_ari = np.mean(ari_scores)
    std_ari = np.std(ari_scores)
    
    print("\n" + "="*50)
    print("📊 CLUSTER STABILITY RESULTS")
    print("="*50)
    print(f"Mean Adjusted Rand Index (ARI): {mean_ari:.4f}")
    print(f"Standard Deviation:             {std_ari:.4f}")
    
    if mean_ari >= 0.90:
        print("Conclusion: Extremely Stable. The clusters are robust to data variations.")
    elif mean_ari >= 0.75:
        print("Conclusion: Highly Stable. The clusters capture strong underlying patterns.")
    elif mean_ari >= 0.50:
        print("Conclusion: Moderately Stable. Clusters shift depending on the specific customers sampled.")
    else:
        print("Conclusion: Unstable. The clustering is highly sensitive to the sample and may not generalize well.")
        
    # Visualization
    out_dir = os.path.join("reports", "clustering")
    os.makedirs(out_dir, exist_ok=True)
    
    plt.figure(figsize=(8, 5))
    sns.histplot(ari_scores, bins=10, kde=True, color='purple')
    plt.axvline(mean_ari, color='red', linestyle='--', label=f'Mean ARI: {mean_ari:.3f}')
    plt.title(f'Cluster Stability over {n_iterations} Bootstrap Samples', fontsize=14)
    plt.xlabel('Adjusted Rand Index (ARI)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend()
    plt.tight_layout()
    
    plot_path = os.path.join(out_dir, '04_stability_distribution.png')
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"\nSaved distribution plot to {plot_path}")
    
if __name__ == "__main__":
    test_stability()
