import pandas as pd
import numpy as np
import os
import sys

def simulate_did():
    try:
        print("--- ValueLens: SYNTHETIC Difference-in-Differences Experiment ---")
        print("WARNING: This is an illustrative simulation using synthetically injected lift, NOT real causal evidence.\n")
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "cleaned_transactions.csv")
        df = pd.read_csv(csv_path)
        df['invoicedate'] = pd.to_datetime(df['invoicedate'])
        
        # Define simulation timeline
        # Dataset runs roughly Dec 2010 to Dec 2011
        # Let's pretend our campaign happened on 2011-09-01
        intervention_date = pd.to_datetime('2011-09-01')
        pre_start = intervention_date - pd.Timedelta(days=60)
        post_end = intervention_date + pd.Timedelta(days=60)
        
        # Filter to our 120 day window
        window_df = df[(df['invoicedate'] >= pre_start) & (df['invoicedate'] <= post_end)].copy()
        
        # Label transactions as pre or post
        window_df['Period'] = np.where(window_df['invoicedate'] < intervention_date, 'Pre', 'Post')
        
        # Aggregate spend per customer per period
        spend_agg = window_df.groupby(['customerid', 'Period'])['totalamount'].sum().unstack(fill_value=0).reset_index()
        
        # We only want customers who existed in the pre-period
        spend_agg = spend_agg[spend_agg['Pre'] > 0].copy()
        
        # Select a random subset to be our "At-Risk" target audience
        np.random.seed(42)
        target_customers = spend_agg.sample(n=min(1000, len(spend_agg)))
        
        # 80/20 Split for Treatment vs Control
        target_customers['Group'] = np.where(np.random.rand(len(target_customers)) < 0.8, 'Treatment', 'Control')
        
        # ---------------------------------------------------------
        # SYNTHETIC LIFT INJECTION & ORGANIC BASELINE
        # We simulate a macroeconomic trend: organic spend DROPS by 15% across all users in the Post period.
        # We inject a £75 average campaign lift into the Treatment group's post-period spend.
        # ---------------------------------------------------------
        synthetic_lift = 75.0
        organic_multiplier = 0.85 # 15% drop
        
        # Simulate Post period based purely on Pre period to control for extreme Whale variance
        # Control Group: Just the organic drop + noise
        control_mask = target_customers['Group'] == 'Control'
        target_customers.loc[control_mask, 'Post'] = target_customers.loc[control_mask, 'Pre'] * organic_multiplier + np.random.normal(0, 10, size=control_mask.sum())
        
        # Treatment Group: Organic drop + Synthetic Lift + noise
        treatment_mask = target_customers['Group'] == 'Treatment'
        target_customers.loc[treatment_mask, 'Post'] = (target_customers.loc[treatment_mask, 'Pre'] * organic_multiplier) + synthetic_lift + np.random.normal(0, 10, size=treatment_mask.sum())
        
        # ---------------------------------------------------------
        # MEASUREMENT (The DiD Calculation)
        # ---------------------------------------------------------
        
        # Calculate means
        means = target_customers.groupby('Group')[['Pre', 'Post']].mean()
        
        Y_T0 = means.loc['Treatment', 'Pre']
        Y_T1 = means.loc['Treatment', 'Post']
        Y_C0 = means.loc['Control', 'Pre']
        Y_C1 = means.loc['Control', 'Post']
        
        # Changes over time
        delta_T = Y_T1 - Y_T0
        delta_C = Y_C1 - Y_C0
        
        # DiD Estimator
        did_estimator = delta_T - delta_C
        
        print(f"Target Audience: {len(target_customers)} customers")
        print(f"Split: {treatment_mask.sum()} Treatment / {control_mask.sum()} Control")
        
        print("\n[Average Customer Spend (£)]")
        print(f"Treatment Pre-Period:  £{Y_T0:.2f}")
        print(f"Treatment Post-Period: £{Y_T1:.2f}  (Change: £{delta_T:+.2f})")
        print(f"Control Pre-Period:    £{Y_C0:.2f}")
        print(f"Control Post-Period:   £{Y_C1:.2f}  (Change: £{delta_C:+.2f})")
        
        print("\n[Difference-in-Differences Result]")
        print(f"Organic Baseline Change (Control): £{delta_C:+.2f}")
        print(f"Gross Treatment Change:            £{delta_T:+.2f}")
        print("-" * 50)
        print(f"Calculated Incremental Lift (DiD): £{did_estimator:+.2f}")
        print(f"Actual Injected Lift (Secret):     £{synthetic_lift:+.2f}")
        
        if abs(did_estimator - synthetic_lift) < 15: # allowing a bit more margin for baseline proportional differences
            print("\nSUCCESS: The DiD methodology successfully filtered out the organic baseline change")
            print("and accurately recovered the true causal impact of the campaign!")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to run simulation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    simulate_did()
