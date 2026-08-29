import pandas as pd
import numpy as np
import os
import sys
from lifetimes import BetaGeoFitter, GammaGammaFitter

def predict_clv():
    try:
        print("--- ValueLens: Predicting 12-Month CLV ---")
        
        # Paths
        processed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
        summary_path = os.path.join(processed_dir, "lifetimes_summary.csv")
        master_path = os.path.join(processed_dir, "customer_rfm.csv")
        
        print(f"Loading lifetimes summary from {summary_path}...")
        summary = pd.read_csv(summary_path)
        
        # Fit BG/NBD
        print("Fitting BG/NBD Model...")
        bgf = BetaGeoFitter(penalizer_coef=0.0)
        bgf.fit(summary['frequency'], summary['recency'], summary['T'])
        
        # Fit Gamma-Gamma (on customers with frequency > 0)
        print("Fitting Gamma-Gamma Model...")
        returning_customers = summary[summary['frequency'] > 0]
        ggf = GammaGammaFitter(penalizer_coef=0.0)
        ggf.fit(returning_customers['frequency'], returning_customers['monetary_value'])
        
        # Predict 12-month CLV
        # time parameter is in months. We have daily data (if T and recency are in days)? 
        # Wait, lifetime_summary time units are based on the original invoice dates.
        # By default, lifetimes summary_data_from_transaction_data uses daily frequency.
        # Wait, if T is in days, then `time=12` in customer_lifetime_value means 12 DAYS! 
        # The documentation for `customer_lifetime_value` states: `time` (float) – the lifetime expected for the user in months. Default: 1.
        # BUT wait! If the model is fitted on days, we must use time in months, but the model assumes time is in months?
        # The lifetimes package `customer_lifetime_value` function specifically expects `time` in MONTHS, and converts it to the model's units (days) internally ONLY if you pass `freq="D"`.
        # Let's specify `freq="D"`.
        
        print("Computing 12-Month Expected CLV per customer...")
        summary['predicted_clv_12m'] = ggf.customer_lifetime_value(
            bgf,
            summary['frequency'],
            summary['recency'],
            summary['T'],
            summary['monetary_value'],
            time=12, # in months
            freq='D', # frequency of T and recency (Days)
            discount_rate=0.01 # standard 1% monthly discount
        )
        
        # Fill missing CLV for brand new/lost customers if any
        summary['predicted_clv_12m'] = summary['predicted_clv_12m'].fillna(0)
        
        print(f"Loading master customer table from {master_path}...")
        master_df = pd.read_csv(master_path)
        
        # Ensure customer ID is matched properly
        # Note: In summary it's 'customerid', in master it's 'CustomerID'
        summary_to_merge = summary[['customerid', 'predicted_clv_12m']].rename(columns={'customerid': 'CustomerID'})
        
        # Merge
        print("Merging CLV predictions into master customer table...")
        if 'predicted_clv_12m' in master_df.columns:
            master_df = master_df.drop(columns=['predicted_clv_12m'])
            
        master_df = master_df.merge(summary_to_merge, on='CustomerID', how='left')
        master_df['predicted_clv_12m'] = master_df['predicted_clv_12m'].fillna(0)
        
        print("Saving updated master table...")
        master_df.to_csv(master_path, index=False)
        
        print("\n[CLV Distribution]")
        print(master_df['predicted_clv_12m'].describe().round(2))
        
        total_predicted_revenue = master_df['predicted_clv_12m'].sum()
        print(f"\nTotal Predicted 12-Month Revenue: £{total_predicted_revenue:,.2f}")
        
        print(f"\n[Success] 12-Month CLV computed and saved to {master_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to predict CLV: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    predict_clv()
