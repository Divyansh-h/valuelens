import pandas as pd
import os
import sys
from lifetimes.utils import summary_data_from_transaction_data

def prepare_lifetimes():
    try:
        print("--- ValueLens: Preparing Data for Lifetimes Package ---")
        
        # Load cleaned transactions
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "cleaned_transactions.csv")
        print(f"Loading transaction history from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        # Convert invoicedate to datetime
        df['invoicedate'] = pd.to_datetime(df['invoicedate'])
        
        # Generate summary using lifetimes utility
        print("Transforming transactions into Frequency, Recency, T, and Monetary Value format...")
        summary_df = summary_data_from_transaction_data(
            transactions=df,
            customer_id_col='customerid',
            datetime_col='invoicedate',
            monetary_value_col='totalamount',
            observation_period_end=df['invoicedate'].max()
        )
        
        print("\n[Lifetimes Summary Sample]")
        print(summary_df.head())
        
        # Save output
        out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "lifetimes_summary.csv")
        summary_df.to_csv(out_path)
        print(f"\n[Success] Successfully saved lifetimes summary to {out_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to prepare lifetimes data: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    prepare_lifetimes()
