import pandas as pd
import os
import pytest

def test_customer_360_integrity():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "data", "processed", "customer_360.csv")
    
    assert os.path.exists(path), "customer_360.csv does not exist"
    
    df = pd.read_csv(path)
    
    # 1. One row per customer (no duplicates)
    assert df['CustomerID'].is_unique, "Duplicate CustomerIDs found"
    
    # 2. Required columns exist
    required_cols = [
        'CustomerID', 'Recency', 'Frequency', 'Monetary', 
        'R_Score', 'F_Score', 'M_Score', 'RFM_Score', 
        'Segment', 'Cluster'
    ]
    for col in required_cols:
        assert col in df.columns, f"Required column missing: {col}"
        
    # 3. No missing analytical fields
    for col in required_cols:
        assert df[col].isnull().sum() == 0, f"Null values found in {col}"
        
    # 4. Consistent data types
    assert pd.api.types.is_numeric_dtype(df['Monetary']), "Monetary should be numeric"
    assert pd.api.types.is_numeric_dtype(df['Frequency']), "Frequency should be numeric"
    assert pd.api.types.is_numeric_dtype(df['Recency']), "Recency should be numeric"
