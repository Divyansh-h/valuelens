import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from clustering import load_and_preprocess_rfm

def plot_clusters_pca():
    print("Loading data for PCA projection...")
    
    # We load the full processed file because it already contains the 'Cluster' assignments
    csv_path = os.path.join("data", "processed", "customer_rfm.csv")
    df = pd.read_csv(csv_path)
    
    # Re-extract features
    rfm_data = df[['Recency', 'Frequency', 'Monetary']].copy()
    rfm_log = np.log1p(rfm_data)
    
    print("Standardizing features and running PCA...")
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_log)
    
    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(rfm_scaled)
    
    df['PCA1'] = pca_result[:, 0]
    df['PCA2'] = pca_result[:, 1]
    
    print(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")
    
    # Sort cluster names for consistent coloring
    clusters = sorted(df['Cluster'].unique())
    
    # Plotting
    print("Generating visualization...")
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='PCA1', 
        y='PCA2', 
        hue='Cluster', 
        hue_order=clusters,
        palette='Set1',
        data=df, 
        alpha=0.6,
        s=40
    )
    
    plt.title('2D PCA Projection of K-Means Clusters', fontsize=16)
    plt.xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
    plt.ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
    plt.legend(title='K-Means Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    out_dir = "reports"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'cluster_viz.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    
    print(f"Saved PCA projection to {out_path}")

if __name__ == "__main__":
    plot_clusters_pca()
