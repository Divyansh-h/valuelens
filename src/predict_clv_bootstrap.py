import pandas as pd
import numpy as np
import os
import sys
from lifetimes import BetaGeoFitter, GammaGammaFitter

def predict_clv_bootstrap():
    try:
        print("--- ValueLens: Bootstrapping CLV Confidence Intervals ---")
        
        # Paths
        processed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
        summary_path = os.path.join(processed_dir, "lifetimes_summary.csv")
        master_path = os.path.join(processed_dir, "customer_rfm.csv")
        
        print(f"Loading lifetimes summary from {summary_path}...")
        summary = pd.read_csv(summary_path)
        
        # Customers with frequency > 0 for Gamma-Gamma
        # To avoid index errors during bootstrapping, we'll keep the original dataframe intact 
        # and sample from it.
        
        n_bootstraps = 100
        n_customers = len(summary)
        
        # We will store predictions for each iteration
        # Matrix shape: (n_customers, n_bootstraps)
        predictions_matrix = np.zeros((n_customers, n_bootstraps))
        
        print(f"Starting {n_bootstraps} bootstrap iterations. This may take a minute...")
        
        for i in range(n_bootstraps):
            if (i+1) % 10 == 0:
                print(f"  Completed {i+1}/{n_bootstraps} iterations...")
                
            # 1. Sample with replacement
            boot_sample = summary.sample(n=n_customers, replace=True, random_state=i)
            
            # 2. Fit BG/NBD on bootstrap sample
            bgf = BetaGeoFitter(penalizer_coef=0.0)
            # Some samples might have issues with fitter if variation is too low, we wrap in try-except
            try:
                bgf.fit(boot_sample['frequency'], boot_sample['recency'], boot_sample['T'])
            except Exception as e:
                # If convergence fails for a random sample, just continue and skip this iteration's contribution for now
                continue
                
            # 3. Fit Gamma-Gamma on bootstrap sample
            boot_returning = boot_sample[boot_sample['frequency'] > 0]
            ggf = GammaGammaFitter(penalizer_coef=0.0)
            try:
                ggf.fit(boot_returning['frequency'], boot_returning['monetary_value'])
            except Exception as e:
                continue
                
            # 4. Predict CLV for ALL ORIGINAL CUSTOMERS using the models trained on the bootstrap sample
            clv_preds = ggf.customer_lifetime_value(
                bgf,
                summary['frequency'],
                summary['recency'],
                summary['T'],
                summary['monetary_value'],
                time=12,
                freq='D',
                discount_rate=0.01
            )
            
            # Fill NaN with 0 for non-returning customers
            predictions_matrix[:, i] = clv_preds.fillna(0).values
            
        print("Bootstrap complete! Calculating percentiles...")
        
        # Calculate 5th, 50th, and 95th percentiles (90% Confidence Interval)
        # Note: If some iterations failed, they will be 0, which could skew.
        # Let's drop columns that are entirely 0 if they failed.
        valid_cols = ~np.all(predictions_matrix == 0, axis=0)
        valid_predictions = predictions_matrix[:, valid_cols]
        
        summary['clv_lower_90ci'] = np.percentile(valid_predictions, 5, axis=1)
        summary['clv_median'] = np.percentile(valid_predictions, 50, axis=1)
        summary['clv_upper_90ci'] = np.percentile(valid_predictions, 95, axis=1)
        
        print(f"Loading master customer table from {master_path}...")
        master_df = pd.read_csv(master_path)
        
        # Merge new columns
        cols_to_merge = ['customerid', 'clv_lower_90ci', 'clv_median', 'clv_upper_90ci']
        summary_to_merge = summary[cols_to_merge].rename(columns={'customerid': 'CustomerID'})
        
        # Drop existing bootstrap columns if they exist
        for col in ['clv_lower_90ci', 'clv_median', 'clv_upper_90ci']:
            if col in master_df.columns:
                master_df = master_df.drop(columns=[col])
                
        master_df = master_df.merge(summary_to_merge, on='CustomerID', how='left')
        
        # Save updated master table
        master_df.to_csv(master_path, index=False)
        
        print("\n[Confidence Interval Stats]")
        master_df['ci_width'] = master_df['clv_upper_90ci'] - master_df['clv_lower_90ci']
        print(master_df[['clv_lower_90ci', 'clv_median', 'clv_upper_90ci', 'ci_width']].describe().round(2))
        
        print("\n[Sample High-Value Customer]")
        whale = master_df.sort_values(by='clv_median', ascending=False).iloc[0]
        print(f"Customer {whale['CustomerID']} ({whale['Segment']})")
        print(f"Lower Bound (5th):  £{whale['clv_lower_90ci']:,.2f}")
        print(f"Median CLV (50th):  £{whale['clv_median']:,.2f}")
        print(f"Upper Bound (95th): £{whale['clv_upper_90ci']:,.2f}")
        print(f"Interval Width:     £{whale['ci_width']:,.2f}")
        
        print(f"\n[Success] Bootstrap CI predictions saved to {master_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to run bootstrap: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    predict_clv_bootstrap()
