import pandas as pd
import numpy as np
import os
import sys
from lifetimes import GammaGammaFitter

def train_gammagamma():
    try:
        print("--- ValueLens: Gamma-Gamma Model Training ---")
        
        # Load summary data
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "lifetimes_summary.csv")
        print(f"Loading lifetimes summary from {csv_path}...")
        summary = pd.read_csv(csv_path)
        
        # The Gamma-Gamma model requires customers who have repeat purchases.
        # The user requested 2+ repeat purchases.
        returning_customers = summary[summary['frequency'] >= 2]
        print(f"Number of customers with 2+ repeat purchases: {len(returning_customers)}")
        
        # Assumption Check: No Correlation between Frequency and Monetary Value
        correlation = returning_customers['frequency'].corr(returning_customers['monetary_value'])
        print(f"\n[Assumption Check]")
        print(f"Pearson Correlation (Frequency vs Monetary Value): {correlation:.4f}")
        
        if abs(correlation) > 0.3:
            print("WARNING: Strong correlation detected. The Gamma-Gamma assumption of independence is violated!")
        else:
            print("Assumption satisfied: Frequency and Monetary Value are largely independent.")
            
        # Fit model
        print("\nFitting Gamma-Gamma Model...")
        ggf = GammaGammaFitter(penalizer_coef=0.0)
        ggf.fit(returning_customers['frequency'], returning_customers['monetary_value'])
        
        print("\n[Gamma-Gamma Model Parameters]")
        print(ggf.summary)
        
        # We can also check if it fits well by comparing average profit to expected average profit
        expected_avg_profit = ggf.conditional_expected_average_profit(
            returning_customers['frequency'],
            returning_customers['monetary_value']
        )
        
        print("\n[Validation]")
        print(f"Actual Mean Monetary Value: £{returning_customers['monetary_value'].mean():.2f}")
        print(f"Expected Mean Monetary Value (Model): £{expected_avg_profit.mean():.2f}")
        
        print("\n[Success] Gamma-Gamma Model trained successfully.")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to train Gamma-Gamma model: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    train_gammagamma()
