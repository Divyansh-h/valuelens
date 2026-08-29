import pandas as pd
import numpy as np
import os
import sys

def build_retention_priority():
    try:
        print("--- ValueLens: Building Retention Priority Score ---")
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        df = pd.read_csv(csv_path)
        
        if 'predicted_clv_12m' not in df.columns:
            raise ValueError("predicted_clv_12m column not found. Please run predict_clv.py first.")
            
        print("Scoring Risk Levels based on RFM Segments...")
        
        # Define risk multipliers based on flight risk
        # Highest priority (1.0) goes to high-value customers at immediate risk of churning
        # Lowest priority (0.2) goes to Champions who are highly engaged and unlikely to churn
        risk_map = {
            'At Risk (High Value)': 1.0,  # Needs immediate intervention
            'Lost': 0.8,                  # Needs reactivation campaign
            'Potential Loyalist': 0.6,    # Needs nurturing
            'Loyal Customers': 0.4,       # Low flight risk
            'Champions': 0.2              # Lowest flight risk, maintain course
        }
        
        df['Risk_Multiplier'] = df['Segment'].map(risk_map)
        
        # If any unexpected segments exist, default to 0.5
        df['Risk_Multiplier'] = df['Risk_Multiplier'].fillna(0.5)
        
        print("Calculating CLV Percentile Ranks...")
        # Rank customers by CLV from 0 (lowest) to 100 (highest)
        df['CLV_Percentile'] = df['predicted_clv_12m'].rank(pct=True) * 100
        
        print("Computing final Combined Retention Priority Score...")
        # A customer in the 99th CLV percentile who is "At Risk" (1.0) gets a score of 99
        # A customer in the 99th CLV percentile who is a "Champion" (0.2) gets a score of 19.8
        df['Retention_Priority_Score'] = df['CLV_Percentile'] * df['Risk_Multiplier']
        
        # Sort by the new priority score
        df = df.sort_values(by='Retention_Priority_Score', ascending=False)
        
        # Select the most important columns for the output list
        output_cols = [
            'CustomerID', 'Segment', 'Cluster', 'Recency', 'Frequency', 'Monetary', 
            'predicted_clv_12m', 'CLV_Percentile', 'Risk_Multiplier', 'Retention_Priority_Score'
        ]
        
        retention_list = df[output_cols].copy()
        
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "retention_priority_list.csv")
        
        retention_list.to_csv(out_path, index=False)
        
        print("\n[Top 5 Highest Priority Customers for Retention]")
        print(retention_list.head(5).to_string(index=False))
        
        print(f"\n[Success] Successfully saved retention priority list to {out_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to build retention priority score: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build_retention_priority()
