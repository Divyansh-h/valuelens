import pandas as pd
import sqlite3
import os
import sys

def analyze_segments():
    try:
        csv_path = os.path.join("data", "processed", "customer_rfm.csv")
        out_path = os.path.join("data", "processed", "segment_summary.csv")
        db_path = os.path.join("database", "valuelens.db")
        
        df = pd.read_csv(csv_path)
        
        # Write the segmented RFM dataset to SQLite for SQL analysis
        print(f"Uploading 'customer_rfm' table to {db_path}...")
        conn = sqlite3.connect(db_path)
        df.to_sql('customer_rfm', conn, if_exists='replace', index=False)
        conn.close()
        
        total_customers = len(df)
        total_revenue = df['Monetary'].sum()
        
        print("Calculating segment metrics...")
        summary = df.groupby('Segment').agg(
            num_customers=('CustomerID', 'count'),
            total_revenue=('Monetary', 'sum'),
            avg_revenue=('Monetary', 'mean'),
            median_revenue=('Monetary', 'median'),
            avg_frequency=('Frequency', 'mean'),
            avg_recency=('Recency', 'mean')
        ).reset_index()
        
        # Add percentages
        summary['pct_customers'] = (summary['num_customers'] / total_customers) * 100
        summary['pct_revenue'] = (summary['total_revenue'] / total_revenue) * 100
        
        # Sort by total revenue descending
        summary = summary.sort_values(by='total_revenue', ascending=False)
        
        # Reorder columns to match the request exactly
        cols = [
            'Segment', 
            'num_customers', 
            'pct_customers', 
            'total_revenue', 
            'pct_revenue', 
            'avg_revenue', 
            'median_revenue', 
            'avg_frequency', 
            'avg_recency'
        ]
        summary = summary[cols]
        
        print(f"Saving summary to {out_path}...\n")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        summary.to_csv(out_path, index=False)
        
        print("--- ValueLens: Business Segment Analysis ---")
        print_summary = summary.copy()
        print_summary['total_revenue'] = print_summary['total_revenue'].map('£{:,.2f}'.format)
        print_summary['avg_revenue'] = print_summary['avg_revenue'].map('£{:,.2f}'.format)
        print_summary['median_revenue'] = print_summary['median_revenue'].map('£{:,.2f}'.format)
        print_summary['pct_customers'] = print_summary['pct_customers'].map('{:.1f}%'.format)
        print_summary['pct_revenue'] = print_summary['pct_revenue'].map('{:.1f}%'.format)
        print_summary['avg_frequency'] = print_summary['avg_frequency'].map('{:.1f}'.format)
        print_summary['avg_recency'] = print_summary['avg_recency'].map('{:.1f} days'.format)
        
        print(print_summary.to_string(index=False))
        
    except Exception as e:
        print(f"\n[ERROR] Analysis Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    analyze_segments()
