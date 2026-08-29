import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from lifetimes import BetaGeoFitter
from lifetimes.plotting import plot_period_transactions

def train_bgnbd():
    try:
        print("--- ValueLens: BG/NBD Model Training ---")
        
        # Load summary data
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "lifetimes_summary.csv")
        print(f"Loading lifetimes summary from {csv_path}...")
        summary = pd.read_csv(csv_path)
        
        # We need positive frequency > 0 for penalizer tuning usually, but base BG/NBD handles zeros
        # Fit model
        print("Fitting Beta-Geometric/NBD Model...")
        bgf = BetaGeoFitter(penalizer_coef=0.0)
        bgf.fit(summary['frequency'], summary['recency'], summary['T'])
        
        print("\n[BG/NBD Model Parameters]")
        print(bgf.summary)
        
        # Diagnostics
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports", "lifetimes")
        os.makedirs(out_dir, exist_ok=True)
        
        print("\nGenerating model fit diagnostic plot (plot_period_transactions)...")
        plt.figure(figsize=(10, 6))
        plot_period_transactions(bgf)
        plt.title('BG/NBD Model Fit: Actual vs Simulated Transactions', fontsize=14)
        
        plot_path = os.path.join(out_dir, "bgnbd_period_transactions.png")
        plt.savefig(plot_path, dpi=300)
        plt.close()
        
        print(f"\n[Success] Diagnostic plot saved to {plot_path}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to train BG/NBD model: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    train_bgnbd()
