import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from clustering import load_and_preprocess_rfm

def evaluate_kmeans():
    # Load preprocessed data
    df, scaled_df, scaler = load_and_preprocess_rfm()
    
    out_dir = os.path.join("reports", "clustering")
    os.makedirs(out_dir, exist_ok=True)
    
    k_range = range(2, 9)
    inertia_values = []
    silhouette_scores = []
    
    results = []
    
    print("Evaluating K-Means for K = 2 to 8...")
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_df)
        
        inertia = kmeans.inertia_
        score = silhouette_score(scaled_df, kmeans.labels_)
        
        inertia_values.append(inertia)
        silhouette_scores.append(score)
        
        results.append({'K': k, 'Inertia': inertia, 'Silhouette_Score': score})
        print(f"K={k}: Inertia={inertia:.2f}, Silhouette={score:.4f}")
        
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(out_dir, 'k_evaluation_metrics.csv'), index=False)
    
    # Visualization 1: Elbow Curve (Inertia)
    plt.figure(figsize=(10, 5))
    plt.plot(k_range, inertia_values, marker='o', linestyle='-', color='royalblue', linewidth=2, markersize=8)
    plt.title('Elbow Method (Inertia vs. Number of Clusters)', fontsize=14, pad=15)
    plt.xlabel('Number of Clusters (K)', fontsize=12)
    plt.ylabel('Inertia (Within-Cluster Sum of Squares)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, '01_elbow_curve.png'), dpi=300)
    plt.close()
    
    # Visualization 2: Silhouette Score Curve
    plt.figure(figsize=(10, 5))
    plt.plot(k_range, silhouette_scores, marker='s', linestyle='-', color='seagreen', linewidth=2, markersize=8)
    plt.title('Silhouette Score vs. Number of Clusters', fontsize=14, pad=15)
    plt.xlabel('Number of Clusters (K)', fontsize=12)
    plt.ylabel('Silhouette Score', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, '02_silhouette_curve.png'), dpi=300)
    plt.close()
    
    print(f"\nEvaluation complete. Results saved to {out_dir}/")

if __name__ == "__main__":
    evaluate_kmeans()
