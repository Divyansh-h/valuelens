import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_skewness():
    """
    Generates before/after histograms showing the effect of the log1p transformation
    on highly skewed RFM features (Frequency and Monetary).
    """
    print("Generating log-transform skewness visualizations...")
    
    # Load RFM Data
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    
    # Setup plotting aesthetics
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('RFM Feature Skewness & Log Transformation (log1p)', fontsize=16, y=1.02)
    
    # 1. Frequency - Before
    sns.histplot(df['Frequency'], bins=50, ax=axes[0, 0], color='salmon')
    axes[0, 0].set_title(f"Original Frequency\nSkewness: {df['Frequency'].skew():.2f}")
    
    # 2. Frequency - After (log1p)
    sns.histplot(np.log1p(df['Frequency']), bins=50, ax=axes[0, 1], color='lightgreen')
    axes[0, 1].set_title(f"Log1p Frequency\nSkewness: {np.log1p(df['Frequency']).skew():.2f}")
    
    # 3. Monetary - Before
    # Exclude extreme outliers for visualization purposes of original data if necessary, 
    # but let's show raw first
    sns.histplot(df['Monetary'], bins=50, ax=axes[1, 0], color='salmon')
    axes[1, 0].set_title(f"Original Monetary\nSkewness: {df['Monetary'].skew():.2f}")
    
    # 4. Monetary - After (log1p)
    # Ensure no negative values break the log1p, cap at 0 for transformation visually
    monetary_safe = df['Monetary'].clip(lower=0)
    sns.histplot(np.log1p(monetary_safe), bins=50, ax=axes[1, 1], color='lightgreen')
    axes[1, 1].set_title(f"Log1p Monetary\nSkewness: {np.log1p(monetary_safe).skew():.2f}")
    
    plt.tight_layout()
    
    # Save output
    os.makedirs(os.path.join("reports", "figures"), exist_ok=True)
    out_path = os.path.join("reports", "figures", "skewness_log_transform.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Successfully saved skewness visualization to {out_path}")

if __name__ == "__main__":
    visualize_skewness()
