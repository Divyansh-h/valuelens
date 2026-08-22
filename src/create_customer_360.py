import sqlite3
import pandas as pd
import os

def create_customer_360():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "database", "valuelens.db")
    rfm_path = os.path.join(base_dir, "data", "processed", "customer_rfm.csv")
    out_path = os.path.join(base_dir, "data", "processed", "customer_360.csv")
    
    # Load RFM + Segment + Cluster
    df = pd.read_csv(rfm_path)
    
    # Justified derived fields:
    # 1. Country (To allow geographic slicing)
    conn = sqlite3.connect(db_path)
    query = "SELECT customerid as CustomerID, MAX(country) as Country FROM sales GROUP BY customerid;"
    df_country = pd.read_sql(query, conn)
    conn.close()
    
    df = pd.merge(df, df_country, on='CustomerID', how='left')
    
    # 2. Average Order Value (AOV) (Critical for scenario modeling/revenue prediction)
    df['AOV'] = df['Monetary'] / df['Frequency']
    
    # Data Quality Constraints
    # Ensure one row per customer
    df = df.drop_duplicates(subset=['CustomerID'])
    
    # Ensure no missing required fields
    required_cols = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score', 'Segment', 'Cluster']
    for col in required_cols:
        if df[col].isnull().any():
            raise ValueError(f"Missing values found in required column: {col}")
            
    # Reorder columns logically
    cols = required_cols + ['AOV', 'Country']
    df = df[cols]
    
    # Save
    df.to_csv(out_path, index=False)
    print(f"Successfully generated clean customer-level analytical dataset: {out_path}")

if __name__ == "__main__":
    create_customer_360()
