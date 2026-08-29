import pandas as pd
import numpy as np
import os
from typing import Tuple, List, Dict, Any, Iterable
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def load_and_preprocess_rfm() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads the RFM dataset and applies necessary transformations for K-Means clustering.
    - Log transformation to handle extreme right-skewness.
    Note: Scaling is deferred to the sklearn Pipeline in the execution scripts.
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Original DataFrame, and log-transformed RFM features.
    """
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    df = pd.read_csv(csv_path)
    
    # 1. Extract core RFM variables
    rfm_data = df[['Recency', 'Frequency', 'Monetary']].copy()
    
    # 2. Log Transformation
    # We use log1p (log(x+1)) to safely handle any potential zero values
    rfm_log = np.log1p(rfm_data)
    
    return df, rfm_log

def find_optimal_k(data: pd.DataFrame, k_range: Iterable[int]) -> Tuple[List[Dict[str, Any]], int]:
    """
    Evaluates different values of K for K-Means clustering using inertia (elbow method) 
    and silhouette score. Uses an 80/20 train-test split to ensure rigorous scaling boundaries.
    
    Args:
        data (pd.DataFrame): The log-transformed RFM features.
        k_range (Iterable[int]): The range of K values to test.
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: A list of dictionaries containing evaluation metrics per K, 
                                          and the optimal K value based on max silhouette score.
    """
    # Split data to ensure standardizer is fitted only on training data
    X_train, X_test = train_test_split(data, test_size=0.2, random_state=42)
    
    results = []
    
    print(f"Evaluating K-Means (in Pipeline) for K in {k_range}...")
    for k in k_range:
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('kmeans', KMeans(n_clusters=k, random_state=42, n_init=10))
        ])
        
        # Fit pipeline purely on the training set
        pipeline.fit(X_train)
        
        # Extract the kmeans model from the pipeline
        kmeans = pipeline.named_steps['kmeans']
        scaler = pipeline.named_steps['scaler']
        
        inertia = kmeans.inertia_
        
        # Silhouette score must be calculated on scaled training data
        X_train_scaled = scaler.transform(X_train)
        score = float(silhouette_score(X_train_scaled, kmeans.labels_))
        
        results.append({
            'K': k, 
            'Inertia': inertia, 
            'Silhouette_Score': score
        })
        print(f"K={k}: Inertia={inertia:.2f}, Silhouette={score:.4f}")
        
    # Find the optimal K (maximize silhouette score)
    best_result = max(results, key=lambda x: x['Silhouette_Score'])
    best_k = best_result['K']
    
    return results, best_k

if __name__ == "__main__":
    df, rfm_log = load_and_preprocess_rfm()
    print("--- Phase 3: Preprocessing Complete ---")
    print("\n[Original Data Skewness]")
    print(df[['Recency', 'Frequency', 'Monetary']].skew())
    print("\n[Log-Transformed Skewness]")
    print(rfm_log.skew())
