import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

def run_cohort_analysis():
    try:
        print("--- ValueLens: Cohort Retention Analysis ---")
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "cleaned_transactions.csv")
        df = pd.read_csv(csv_path)
        
        # Convert invoicedate to datetime
        df['invoicedate'] = pd.to_datetime(df['invoicedate'])
        
        # 1. Create a function to extract Year-Month
        def get_month(x):
            return pd.Timestamp(x.year, x.month, 1)
            
        df['InvoiceMonth'] = df['invoicedate'].apply(get_month)
        
        # 2. Find the Acquisition Month for each customer
        grouping = df.groupby('customerid')['InvoiceMonth']
        df['CohortMonth'] = grouping.transform('min')
        
        # 3. Calculate Cohort Index (number of months since acquisition)
        def get_date_int(df, column):
            year = df[column].dt.year
            month = df[column].dt.month
            return year, month
            
        invoice_year, invoice_month = get_date_int(df, 'InvoiceMonth')
        cohort_year, cohort_month = get_date_int(df, 'CohortMonth')
        
        years_diff = invoice_year - cohort_year
        months_diff = invoice_month - cohort_month
        
        # Cohort Index: 0 = acquisition month, 1 = first month after, etc.
        df['CohortIndex'] = years_diff * 12 + months_diff
        
        # 4. Count unique customers per CohortMonth and CohortIndex
        cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['customerid'].nunique().reset_index()
        
        # 5. Pivot into a matrix (CohortMonth as index, CohortIndex as columns)
        cohort_counts = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='customerid')
        
        # 6. Calculate Retention Rates
        cohort_sizes = cohort_counts.iloc[:, 0]
        retention = cohort_counts.divide(cohort_sizes, axis=0)
        
        # Format index to string YYYY-MM for cleaner plots
        retention.index = retention.index.strftime('%Y-%m')
        
        print("Cohort Matrix Created.")
        
        # Set up output directory
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
        os.makedirs(out_dir, exist_ok=True)
        
        # 7. Plot 1: Retention Heatmap
        plt.figure(figsize=(14, 8))
        sns.heatmap(retention, annot=True, fmt='.0%', cmap='YlGnBu', vmin=0.0, vmax=0.5)
        plt.title('Cohort Retention Heatmap (Percentage of Active Customers)', fontsize=16)
        plt.xlabel('Months Since Acquisition', fontsize=12)
        plt.ylabel('Cohort (Acquisition Month)', fontsize=12)
        plt.tight_layout()
        heatmap_path = os.path.join(out_dir, "cohort_retention_heatmap.png")
        plt.savefig(heatmap_path, dpi=300)
        plt.close()
        
        # 8. Plot 2: Retention Curves (Line Plot)
        plt.figure(figsize=(12, 8))
        
        # We'll plot the first 6 cohorts to keep the graph readable
        for i, cohort in enumerate(retention.index[:6]):
            plt.plot(retention.columns, retention.loc[cohort], marker='o', linewidth=2, label=cohort)
            
        plt.title('Cohort Retention Curves (First 6 Cohorts)', fontsize=16)
        plt.xlabel('Months Since Acquisition', fontsize=12)
        plt.ylabel('Retention Rate', fontsize=12)
        plt.ylim(0, 1)
        plt.xticks(np.arange(0, retention.columns.max() + 1, 1))
        plt.legend(title='Cohort', loc='upper right')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        curves_path = os.path.join(out_dir, "cohort_retention_curves.png")
        plt.savefig(curves_path, dpi=300)
        plt.close()
        
        print(f"[Success] Generated heatmap: {heatmap_path}")
        print(f"[Success] Generated curves:  {curves_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to run cohort analysis: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_cohort_analysis()
