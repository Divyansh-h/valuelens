import pandas as pd
import os
import sys

def assign_segment(row):
    """
    Assigns a business segment based on predefined RFM (Recency, Frequency) rules.
    Order matters due to overlapping conditions. The first matching rule wins.
    """
    r = row['R_Score']
    f = row['F_Score']
    
    if r >= 4 and f >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3:
        return 'Loyal Customers'
    elif r <= 2 and f >= 4:
        return 'At Risk (High Value)'
    elif r <= 2 and f <= 2:
        return 'Lost'
    else:
        return 'Potential Loyalist'

def run_segmentation():
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        
        print(f"Loading RFM data from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        print("Applying business segmentation rules...")
        # Apply function row by row
        df['Segment'] = df.apply(assign_segment, axis=1)
        
        # Reorder columns slightly for analytical convenience
        cols = ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score', 'Segment']
        df = df[cols]
        
        print(f"Saving segmented data back to {csv_path}...")
        df.to_csv(csv_path, index=False)
        
        print("\n--- Segmentation Summary ---")
        counts = df['Segment'].value_counts()
        for segment, count in counts.items():
            pct = (count / len(df)) * 100
            print(f"{segment:<25}: {count:>5} ({pct:>5.1f}%)")
            
        print("\nSegmentation complete.")
        
    except Exception as e:
        print(f"\n[ERROR] Segmentation Pipeline Failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_segmentation()
