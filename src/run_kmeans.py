import pandas as pd
import os
import sys
from sklearn.cluster import KMeans
from clustering import load_and_preprocess_rfm

import yaml

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_final_clustering():
    try:
        config = load_config()
        k = config['machine_learning']['k_clusters']
        
        print("--- ValueLens: Phase 3 K-Means Execution ---")
        print("Loading and preprocessing RFM data (Log-Transform)...")
        df, rfm_log = load_and_preprocess_rfm()
        
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        
        print("Splitting data to fit standardizer strictly on training data...")
        X_train, X_test = train_test_split(rfm_log, test_size=0.2, random_state=42)
        
        print(f"Building pipeline: StandardScaler -> KMeans(k={k})")
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=k, random_state=42, n_init=10))
        ])
        
        print("Fitting pipeline on training data...")
        pipeline.fit(X_train)
        
        print("Predicting clusters across the entire dataset...")
        # Assign neutral cluster labels to preserve algorithmic purity before business interpretation
        df['Cluster'] = [f"Cluster {label}" for label in pipeline.predict(rfm_log)]
        
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
