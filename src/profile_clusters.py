import pandas as pd
import os
import sys

def profile_clusters():
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports", "clustering")
        out_csv = os.path.join(out_dir, "cluster_profiles.csv")
        
        os.makedirs(out_dir, exist_ok=True)
        
        df = pd.read_csv(csv_path)
        total_customers = len(df)
        total_revenue = df['Monetary'].sum()
        
        summary = df.groupby('Cluster').agg(
            num_customers=('CustomerID', 'count'),
            avg_recency=('Recency', 'mean'),
            median_recency=('Recency', 'median'),
            avg_frequency=('Frequency', 'mean'),
            avg_monetary=('Monetary', 'mean'),
            median_monetary=('Monetary', 'median'),
            total_revenue=('Monetary', 'sum')
        ).reset_index()
        
        summary['pct_customers'] = (summary['num_customers'] / total_customers) * 100
        summary['pct_revenue'] = (summary['total_revenue'] / total_revenue) * 100
        
        # Sort clusters by total revenue descending just to see importance easily
        summary = summary.sort_values(by='total_revenue', ascending=False)
        
        # Reorder columns
        cols = [
            'Cluster', 'num_customers', 'pct_customers', 
            'avg_recency', 'median_recency', 'avg_frequency', 
            'avg_monetary', 'median_monetary', 'total_revenue', 'pct_revenue'
        ]
        summary = summary[cols]
        
        summary.to_csv(out_csv, index=False)
        
        print("--- ValueLens: K-Means Cluster Profiles ---")
        print_summary = summary.copy()
        print_summary['pct_customers'] = print_summary['pct_customers'].map('{:.1f}%'.format)
        print_summary['pct_revenue'] = print_summary['pct_revenue'].map('{:.1f}%'.format)
        print_summary['avg_recency'] = print_summary['avg_recency'].map('{:.1f}'.format)
        print_summary['median_recency'] = print_summary['median_recency'].map('{:.1f}'.format)
        print_summary['avg_frequency'] = print_summary['avg_frequency'].map('{:.1f}'.format)
        print_summary['avg_monetary'] = print_summary['avg_monetary'].map('£{:,.2f}'.format)
        print_summary['median_monetary'] = print_summary['median_monetary'].map('£{:,.2f}'.format)
        print_summary['total_revenue'] = print_summary['total_revenue'].map('£{:,.2f}'.format)
        
        print(print_summary.to_string(index=False))
        
        print(f"\nSaved cluster profile to {out_csv}")
        
    except Exception as e:
        print(f"\n[ERROR] Profiling Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    profile_clusters()
