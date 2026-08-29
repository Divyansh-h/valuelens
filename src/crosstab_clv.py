import pandas as pd
import numpy as np
import os
import sys

def crosstab_clv():
    try:
        print("--- ValueLens: Cross-tabulating RFM Segments vs CLV Quartiles ---")
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        df = pd.read_csv(csv_path)
        
        if 'predicted_clv_12m' not in df.columns:
            raise ValueError("predicted_clv_12m column not found. Please run predict_clv.py first.")
            
        # Bucket CLV into Quartiles
        print("Bucketing customers into CLV quartiles...")
        quartile_labels = ['Q1 (Low)', 'Q2 (Med-Low)', 'Q3 (Med-High)', 'Q4 (High)']
        
        # We use qcut to create quartiles. Sometimes many users might have same predicted CLV (e.g., 0).
        # To avoid bin edges overlapping, we use duplicates='drop' or add tiny noise.
        # But we know CLV varies a lot.
        df['CLV_Quartile'] = pd.qcut(df['predicted_clv_12m'], q=4, labels=quartile_labels, duplicates='drop')
        
        print("\n[Cross-Tabulation: RFM Segment vs CLV Quartile]")
        crosstab = pd.crosstab(df['Segment'], df['CLV_Quartile'])
        print(crosstab)
        
        # Save crosstab
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        crosstab_path = os.path.join(reports_dir, "segment_clv_crosstab.csv")
        crosstab.to_csv(crosstab_path)
        print(f"\nSaved cross-tabulation table to {crosstab_path}")
        
        # Identify mismatches
        print("\n[Identifying Mismatches]")
        # 1. "At Risk (High Value)" or "Lost" customers who are in Q4 (High)
        mismatch_atrisk_q4 = df[(df['Segment'].isin(['At Risk (High Value)', 'Lost'])) & (df['CLV_Quartile'] == 'Q4 (High)')]
        
        # 2. "Champions" or "Loyal Customers" who are in Q1 (Low)
        mismatch_champ_q1 = df[(df['Segment'].isin(['Champions', 'Loyal Customers'])) & (df['CLV_Quartile'] == 'Q1 (Low)')]
        
        print(f"Found {len(mismatch_atrisk_q4)} customers labeled 'At Risk/Lost' but in Top CLV Quartile (Q4)!")
        print(f"Found {len(mismatch_champ_q1)} customers labeled 'Champions/Loyal Customers' but in Bottom CLV Quartile (Q1)!")
        
        # Combine mismatches
        mismatches = pd.concat([mismatch_atrisk_q4, mismatch_champ_q1])
        mismatches_path = os.path.join(reports_dir, "clv_segment_mismatches.csv")
        mismatches.to_csv(mismatches_path, index=False)
        
        print(f"Saved {len(mismatches)} total mismatches to {mismatches_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to cross-tabulate: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    crosstab_clv()
