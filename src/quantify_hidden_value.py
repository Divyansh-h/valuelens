import pandas as pd
import os
import sys

def quantify_hidden_value():
    try:
        print("--- ValueLens: Quantifying Hidden Value Segment ---")
        
        mismatches_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports", "clv_segment_mismatches.csv")
        
        if not os.path.exists(mismatches_path):
            raise FileNotFoundError(f"Could not find mismatches report at {mismatches_path}")
            
        df = pd.read_csv(mismatches_path)
        
        # Isolate At-Risk/Lost but Q4
        hidden_gems = df[(df['Segment'].isin(['At Risk (High Value)', 'Lost'])) & (df['CLV_Quartile'] == 'Q4 (High)')]
        
        count = len(hidden_gems)
        total_revenue_at_stake = hidden_gems['predicted_clv_12m'].sum()
        avg_revenue = hidden_gems['predicted_clv_12m'].mean()
        
        print("\n[Hidden Value Segment Analysis]")
        print(f"Number of 'Hidden Gem' Customers: {count}")
        print(f"Average 12-Month CLV per Customer: £{avg_revenue:,.2f}")
        print(f"Total Revenue At Stake: £{total_revenue_at_stake:,.2f}")
        
        print("\nConclusion: If marketing relies strictly on RFM heuristics and abandons these 'Lost/At-Risk' customers,")
        print(f"the business risks permanently losing out on roughly £{total_revenue_at_stake/1e6:.1f} Million in forecasted revenue over the next 12 months.")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to quantify hidden value: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    quantify_hidden_value()
