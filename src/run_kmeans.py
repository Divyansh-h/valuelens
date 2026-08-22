import pandas as pd
import os
import sys
from sklearn.cluster import KMeans
from clustering import load_and_preprocess_rfm

def run_final_clustering():
    try:
        print("--- ValueLens: Phase 3 K-Means Execution ---")
        print("Loading and preprocessing RFM data (Log-Transform + StandardScaler)...")
        df, scaled_df, scaler = load_and_preprocess_rfm()
        
        # We selected K=4 based on the Inertia Elbow and Silhouette analysis
        k = 4
        print(f"Running K-Means clustering with K={k} (random_state=42, n_init=10)...")
        
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_df)
        
        # Assign neutral cluster labels to preserve algorithmic purity before business interpretation
        df['Cluster'] = [f"Cluster {label}" for label in kmeans.labels_]
        
        # Ensure 'Cluster' is appended cleanly without losing any original metrics
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        
        print(f"Saving cluster assignments back to {csv_path}...")
        df.to_csv(csv_path, index=False)
        
        print("\n--- Algorithm Cluster Distribution ---")
        counts = df['Cluster'].value_counts().sort_index()
        for cluster, count in counts.items():
            print(f"{cluster}: {count} customers")
            
        print("\n[Success] Final Clustering complete.")
        
    except Exception as e:
        print(f"\n[ERROR] Clustering Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_final_clustering()
