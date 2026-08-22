import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

def load_and_preprocess_rfm():
    """
    Loads the RFM dataset and applies necessary transformations for K-Means clustering.
    - Log transformation to handle extreme right-skewness.
    - StandardScaler to equalize variance for distance calculations.
    """
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    df = pd.read_csv(csv_path)
    
    # 1. Extract core RFM variables
    rfm_data = df[['Recency', 'Frequency', 'Monetary']].copy()
    
    # 2. Log Transformation
    # We use log1p (log(x+1)) to safely handle any potential zero values, 
    # though our data rules guarantee Recency >= 1, Frequency >= 1, Monetary > 0.
    rfm_log = np.log1p(rfm_data)
    
    # 3. Standardization
    # K-Means uses Euclidean distance, making it extremely sensitive to scale.
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_log)
    
    # Convert back to DataFrame for easy handling
    rfm_scaled_df = pd.DataFrame(rfm_scaled, index=df.index, columns=rfm_data.columns)
    
    return df, rfm_scaled_df, scaler

if __name__ == "__main__":
    df, scaled_df, scaler = load_and_preprocess_rfm()
    print("--- Phase 3: Preprocessing Complete ---")
    print("\n[Original Data Skewness]")
    print(df[['Recency', 'Frequency', 'Monetary']].skew())
    print("\n[Log-Transformed Skewness]")
    print(np.log1p(df[['Recency', 'Frequency', 'Monetary']]).skew())
    print("\n[Standardized Data Validation]")
    print(f"Means (should be ~0): {np.round(scaled_df.mean().values, 4)}")
    print(f"StDevs (should be ~1): {np.round(scaled_df.std().values, 4)}")
