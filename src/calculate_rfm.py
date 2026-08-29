import sqlite3
import pandas as pd
import os
import yaml

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yaml")
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def calculate_rfm():
    """Executes the RFM SQL query and returns the results as a DataFrame."""
    config = load_config()
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "valuelens.db")
    sql_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")
    export_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # Determine reference date
    ref_date = config['pipeline']['analysis_reference_date']
    if ref_date == 'dynamic':
        # Get max date from stg_sales
        # Since stg_sales doesn't exist yet as a view in this session, we query the raw 'sales' table
        max_date_query = "SELECT date(MAX(invoicedate)) FROM sales"
        ref_date = conn.execute(max_date_query).fetchone()[0]
        # Format for SQLite date function
        ref_date_sql = f"'{ref_date}'"
    else:
        ref_date_sql = f"'{ref_date}'"
        
    lookback = config['pipeline']['lookback_window_in_months']
    quintiles = config['rfm']['number_of_quintiles']
    
    print("Reading final longitudinal RFM calculation via SQL...")
    # The views (stg_sales, int_monthly_snapshots, etc) are already created by run_pipeline.py
    
    with open(os.path.join(sql_dir, "marts", "mart_customer_rfm_scores_monthly.sql"), 'r') as f:
        mart_sql = f.read()
        mart_sql = mart_sql.replace('{NUM_QUINTILES}', str(quintiles))
    
    print("Executing final longitudinal RFM calculation via SQL...")
    df_rfm = pd.read_sql(mart_sql, conn)
    
    # Rename columns to match the requested clean analytical dataset format
    df_rfm.rename(columns={
        'customerid': 'CustomerID',
        'snapshot_date': 'Snapshot_Date',
        'recency_days': 'Recency',
        'frequency': 'Frequency',
        'monetary': 'Monetary',
        'r_score': 'R_Score',
        'f_score': 'F_Score',
        'm_score': 'M_Score'
    }, inplace=True)
    
    # Combine scores to form a traditional RFM Segment string (e.g. '555')
    df_rfm['RFM_Score'] = df_rfm['R_Score'].astype(str) + df_rfm['F_Score'].astype(str) + df_rfm['M_Score'].astype(str)
    
    print(f"RFM analysis completed for {len(df_rfm)} customer-months.")
    
    # Keep only the requested columns
    cols = ['CustomerID', 'Snapshot_Date', 'Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score']
    df_rfm = df_rfm[cols]
    
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    df_rfm.to_csv(export_path, index=False)
    print(f"Saved clean analytical dataset to {export_path}")
    
    conn.close()
    return df_rfm

if __name__ == "__main__":
    calculate_rfm()
