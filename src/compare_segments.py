import pandas as pd
import os
import sys

def compare_segments():
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        df = pd.read_csv(csv_path)
        
        # Reorder segments logically for better reading
        segment_order = ['Champions', 'Loyal Customers', 'Potential Loyalist', 'At Risk (High Value)', 'Lost']
        df['Segment'] = pd.Categorical(df['Segment'], categories=segment_order, ordered=True)
        
        # Reorder clusters by the previously identified numeric values 1 (Whales), 0 (Core), 2 (New), 3 (Lost)
        cluster_order = ['Cluster 1', 'Cluster 0', 'Cluster 2', 'Cluster 3']
        df['Cluster'] = pd.Categorical(df['Cluster'], categories=cluster_order, ordered=True)
        
        # Cross-tabulation: Counts
        crosstab_counts = pd.crosstab(df['Segment'], df['Cluster'])
        
        # Row Percentages (How each Business Segment is distributed across Clusters)
        crosstab_row_pct = pd.crosstab(df['Segment'], df['Cluster'], normalize='index') * 100
        
        # Column Percentages (How each Cluster is composed of Business Segments)
        crosstab_col_pct = pd.crosstab(df['Segment'], df['Cluster'], normalize='columns') * 100
        
        print("--- CROSS-TABULATION: COUNTS ---")
        print(crosstab_counts)
        
        print("\n--- ROW PERCENTAGES (Segment Breakdown by Algorithmic Cluster) ---")
        print(crosstab_row_pct.round(1))
        
        print("\n--- COLUMN PERCENTAGES (Algorithmic Cluster Breakdown by Segment) ---")
        print(crosstab_col_pct.round(1))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    compare_segments()
