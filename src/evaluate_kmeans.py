import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from clustering import load_and_preprocess_rfm, find_optimal_k

def evaluate_kmeans():
    # Load preprocessed data (log-transformed)
    df, rfm_log = load_and_preprocess_rfm()
    
    out_dir = os.path.join("reports", "clustering")
    os.makedirs(out_dir, exist_ok=True)
    
    k_range = range(2, 11)
    
    print("Finding optimal K...")
    results, best_k = find_optimal_k(rfm_log, k_range)
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(out_dir, 'k_evaluation_metrics.csv'), index=False)
    
    # Visualization: Side-by-side Elbow and Silhouette
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Elbow Curve (Inertia)
    ax1.plot(results_df['K'], results_df['Inertia'], marker='o', linestyle='-', color='royalblue', linewidth=2, markersize=8)
    ax1.set_title('Elbow Method (Inertia vs. Clusters)', fontsize=14, pad=15)
    ax1.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax1.set_ylabel('Inertia', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Silhouette Score Curve
    ax2.plot(results_df['K'], results_df['Silhouette_Score'], marker='s', linestyle='-', color='seagreen', linewidth=2, markersize=8)
    ax2.set_title('Silhouette Score vs. Clusters', fontsize=14, pad=15)
    ax2.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax2.set_ylabel('Silhouette Score', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    out_path = os.path.join(out_dir, 'k_evaluation_combined.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    
    best_silhouette = results_df[results_df['K'] == best_k]['Silhouette_Score'].iloc[0]
    
    print("\n" + "="*50)
    print("📈 K-MEANS OPTIMIZATION RECOMMENDATION")
    print("="*50)
    print(f"Recommended K: {best_k}")
    print(f"Justification: K={best_k} achieves the highest silhouette score ({best_silhouette:.4f}) across all tested values.")
    print("This indicates that the clusters are highly cohesive and well-separated from one another at this value.")
    print("To confirm, cross-reference this with the elbow curve plot where the inertia descent begins to flatten.")
    print(f"\nSaved combined visualization to {out_path}")
    print("Evaluation complete.")

if __name__ == "__main__":
    evaluate_kmeans()
