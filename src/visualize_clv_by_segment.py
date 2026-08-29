import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

def visualize_clv():
    try:
        print("--- ValueLens: Visualizing CLV by RFM Segment ---")
        
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
        df = pd.read_csv(csv_path)
        
        if 'predicted_clv_12m' not in df.columns:
            raise ValueError("predicted_clv_12m column not found. Please run predict_clv.py first.")
            
        print("Creating visualizations...")
        
        # Filter out 0 or negative CLV for log-scale plotting
        # Though Gamma-Gamma CLV should be strictly positive, we added 0 for missing values.
        df_plot = df[df['predicted_clv_12m'] > 1].copy()
        
        plt.figure(figsize=(14, 8))
        
        # We use a violin plot with a log-scale on the Y axis due to extreme outliers ("Whales")
        ax = sns.violinplot(
            data=df_plot,
            x='Segment',
            y='predicted_clv_12m',
            palette='viridis',
            inner='quartile' # Show quartiles inside the violin
        )
        
        ax.set_yscale('log')
        plt.title('Distribution of 12-Month CLV by RFM Segment (Log Scale)', fontsize=16, pad=20)
        plt.xlabel('Static RFM Segment', fontsize=12)
        plt.ylabel('Predicted 12-Month CLV (£) [Log Scale]', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adding some annotations
        plt.tight_layout()
        
        # Save plot
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "clv_by_segment.png")
        
        plt.savefig(out_path, dpi=300)
        plt.close()
        
        print(f"\n[Success] Successfully saved CLV distribution visualization to {out_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to visualize CLV: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    visualize_clv()
