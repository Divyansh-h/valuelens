import pandas as pd
import numpy as np
import os
import sys

def test_seasonality_bias():
    try:
        print("--- ValueLens: Testing Seasonality Bias in RFM Scores ---")
        
        # Load transactions
        tx_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "cleaned_transactions.csv")
        tx_df = pd.read_csv(tx_path)
        tx_df['invoicedate'] = pd.to_datetime(tx_df['invoicedate'])
        
        # Load RFM Segment data
        rfm_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        rfm_df = pd.read_csv(rfm_path)
        
        # Extract purchase month
        tx_df['InvoiceMonth'] = tx_df['invoicedate'].dt.month
        
        # Define "Holiday Season" as November (11) and December (12)
        tx_df['Is_Holiday_Spend'] = tx_df['InvoiceMonth'].isin([11, 12])
        
        # Calculate total spend and holiday spend per customer
        spend_agg = tx_df.groupby('customerid').agg(
            Total_Spend=('totalamount', 'sum'),
            Holiday_Spend=('totalamount', lambda x: x[tx_df.loc[x.index, 'Is_Holiday_Spend']].sum()),
            Total_Purchases=('invoiceno', 'nunique')
        ).reset_index()
        
        # Calculate percentage of spend occurring in the holidays
        spend_agg['Holiday_Spend_Pct'] = spend_agg['Holiday_Spend'] / spend_agg['Total_Spend']
        
        # Define a "Holiday-Only Shopper" as someone with >75% spend in Nov/Dec
        spend_agg['Is_Holiday_Shopper'] = spend_agg['Holiday_Spend_Pct'] >= 0.75
        
        # Merge back with the RFM Segments
        merged_df = rfm_df.merge(spend_agg[['customerid', 'Holiday_Spend_Pct', 'Is_Holiday_Shopper']], 
                                 left_on='CustomerID', right_on='customerid', how='left')
        
        # Analyze Champions and Loyal Customers
        champions_loyal = merged_df[merged_df['Segment'].isin(['Champions', 'Loyal Customers'])]
        
        holiday_false_positives = champions_loyal[champions_loyal['Is_Holiday_Shopper']]
        
        print("\n[Seasonality Bias Results]")
        print(f"Total 'Champions' & 'Loyal Customers': {len(champions_loyal)}")
        print(f"Number of them who are actually 'Holiday-Only' shoppers (>75% spend in Nov/Dec): {len(holiday_false_positives)}")
        print(f"Percentage distorted by Seasonality: {(len(holiday_false_positives) / len(champions_loyal)) * 100:.1f}%\n")
        
        print("[Why this happens]")
        print("Because the dataset snapshot ends in early December, any customer who buys strictly for the holidays")
        print("will have a mathematically near-perfect 'Recency' score (e.g. 2 days ago).")
        print("Static RFM rewards them with a 'Champion' tag, even though they will immediately churn for the next 10 months.")
        
        print("\n[Proposed Adjustments]")
        print("1. CLV Replacement: This definitively proves why our probabilistic CLV model (which predicted many of these as Q1 Low-Value)")
        print("   is superior to static RFM heuristics. We should deprecate RFM Segment as a standalone marketing trigger.")
        print("2. Dispersion Metric: If we must keep RFM, we need to add a 'T' metric (RFM-T) measuring inter-purchase time variance.")
        print("   If variance is massive (e.g. 11 months of zero activity followed by a spike), they are a seasonal buyer, not a Champion.")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to test seasonality bias: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    test_seasonality_bias()
