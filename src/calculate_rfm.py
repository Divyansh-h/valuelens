import sqlite3
import pandas as pd
import os

def calculate_rfm():
    """Executes the RFM SQL query and returns the results as a DataFrame."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "valuelens.db")
    sql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql", "02_rfm_analysis.sql")
    export_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    
    with open(sql_path, 'r') as f:
        query = f.read()
        
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    print("Executing RFM calculation via SQL...")
    df_rfm = pd.read_sql(query, conn)
    
    # Rename columns to match the requested clean analytical dataset format
    df_rfm.rename(columns={
        'customerid': 'CustomerID',
        'recency_days': 'Recency',
        'frequency': 'Frequency',
        'monetary': 'Monetary',
        'r_score': 'R_Score',
        'f_score': 'F_Score',
        'm_score': 'M_Score'
    }, inplace=True)
    
    # Combine scores to form a traditional RFM Segment string (e.g. '555')
    df_rfm['RFM_Score'] = df_rfm['R_Score'].astype(str) + df_rfm['F_Score'].astype(str) + df_rfm['M_Score'].astype(str)
    
    print(f"RFM analysis completed for {len(df_rfm)} customers.")
    
    # Keep only the requested columns
    cols = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score']
    df_rfm = df_rfm[cols]
    
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    df_rfm.to_csv(export_path, index=False)
    print(f"Saved clean analytical dataset to {export_path}")
    
    conn.close()
    return df_rfm
