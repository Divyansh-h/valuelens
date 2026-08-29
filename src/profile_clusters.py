import pandas as pd
import os
import numpy as np

def profile_clusters():
    print("Loading data for cluster profiling...")
    csv_path = os.path.join("data", "processed", "customer_rfm.csv")
    df = pd.read_csv(csv_path)
    
    # Calculate totals for percentage share
    total_customers = len(df)
    total_revenue = df['Monetary'].sum()
    
    # Group and aggregate
    profiles = df.groupby('Cluster').agg({
        'CustomerID': 'count',
        'Recency': ['mean', 'median'],
        'Frequency': ['mean', 'median'],
        'Monetary': ['mean', 'median', 'sum']
    })
    
    # Flatten multi-index columns
    profiles.columns = [
        'Customer_Count', 
        'Recency_Mean', 'Recency_Median',
        'Frequency_Mean', 'Frequency_Median',
        'Monetary_Mean', 'Monetary_Median', 'Total_Revenue'
    ]
    
    # Add calculated columns
    profiles['Pct_of_Customers'] = (profiles['Customer_Count'] / total_customers * 100).round(2)
    profiles['Pct_of_Revenue'] = (profiles['Total_Revenue'] / total_revenue * 100).round(2)
    
    # Reorder columns for readability
    cols_order = [
        'Customer_Count', 'Pct_of_Customers',
        'Total_Revenue', 'Pct_of_Revenue',
        'Recency_Mean', 'Recency_Median',
        'Frequency_Mean', 'Frequency_Median',
        'Monetary_Mean', 'Monetary_Median'
    ]
    profiles = profiles[cols_order].copy()
    
    # Round numerical columns logically
    for col in profiles.columns:
        if 'Mean' in col or 'Median' in col or 'Revenue' in col:
            profiles[col] = profiles[col].round(2)
            
    # Reset index to make 'Cluster' a regular column
    profiles.reset_index(inplace=True)
    
    # Export to CSV
    out_dir = "reports"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cluster_profiles.csv")
    profiles.to_csv(out_path, index=False)
    
    print("\n--- Cluster Profiles ---")
    print(profiles.to_string(index=False))
    print(f"\nSaved profile table to {out_path}")

if __name__ == "__main__":
    profile_clusters()
