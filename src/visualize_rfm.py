import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def visualize_rfm():
    csv_path = os.path.join("data", "processed", "customer_rfm.csv")
    fig_dir = os.path.join("reports", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    
    df = pd.read_csv(csv_path)
    
    # ---------------------------------------------------------
    # Statistical Analysis (Skewness & Outliers)
    # ---------------------------------------------------------
    print("--- ValueLens: RFM Exploratory Analysis ---")
    
    print("\n[Skewness]")
    print(f"Recency Skewness:   {df['Recency'].skew():.2f} (Moderate right skew)")
    print(f"Frequency Skewness: {df['Frequency'].skew():.2f} (Extreme right skew)")
    print(f"Monetary Skewness:  {df['Monetary'].skew():.2f} (Extreme right skew)")
    
    print("\n[Percentiles (95th & 99th)]")
    print(f"Frequency 95th: {df['Frequency'].quantile(0.95):.0f} | 99th: {df['Frequency'].quantile(0.99):.0f} | Max: {df['Frequency'].max():.0f}")
    print(f"Monetary 95th: £{df['Monetary'].quantile(0.95):,.2f} | 99th: £{df['Monetary'].quantile(0.99):,.2f} | Max: £{df['Monetary'].max():,.2f}")
    
    print("\nNote: Because Frequency and Monetary exhibit extreme right-skewness (massive B2B wholesale outliers), log transformation is highly recommended for visual scaling and future K-Means modeling. The raw business values remain unmodified.")
    
    # ---------------------------------------------------------
    # Visualizations Settings
    # ---------------------------------------------------------
    sns.set_theme(style="whitegrid", palette="muted")
    
    # 1. Recency Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Recency'], bins=50, kde=True, color='royalblue')
    plt.title('Recency Distribution (Days Since Last Purchase)', fontsize=14, pad=15)
    plt.xlabel('Recency (Days)', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '01_recency_distribution.png'), dpi=300)
    plt.close()
    
    # 2. Frequency Distribution (Log Scale)
    plt.figure(figsize=(10, 6))
    # We apply log10 scaling to the x-axis to visualize the extreme spread
    sns.histplot(df['Frequency'], bins=30, log_scale=True, color='seagreen')
    plt.title('Frequency Distribution (Log Scale)', fontsize=14, pad=15)
    plt.xlabel('Frequency (Number of Invoices) [Log10 Scale]', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '02_frequency_distribution.png'), dpi=300)
    plt.close()
    
    # 3. Monetary Distribution (Log Scale)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Monetary'], bins=40, log_scale=True, color='indigo')
    plt.title('Monetary Distribution (Log Scale)', fontsize=14, pad=15)
    plt.xlabel('Monetary Value (£) [Log10 Scale]', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '03_monetary_distribution.png'), dpi=300)
    plt.close()
    
    # 4. R-Score Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(x='R_Score', data=df, palette='Blues_d')
    plt.title('Recency Score (R-Score) Distribution', fontsize=14)
    plt.xlabel('R Score (5 is Most Recent)', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '04_r_score_distribution.png'), dpi=300)
    plt.close()
    
    # 5. F-Score Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(x='F_Score', data=df, palette='Greens_d')
    plt.title('Frequency Score (F-Score) Distribution', fontsize=14)
    plt.xlabel('F Score (5 is Most Frequent)', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '05_f_score_distribution.png'), dpi=300)
    plt.close()
    
    # 6. M-Score Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(x='M_Score', data=df, palette='Purples_d')
    plt.title('Monetary Score (M-Score) Distribution', fontsize=14)
    plt.xlabel('M Score (5 is Highest Spend)', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '06_m_score_distribution.png'), dpi=300)
    plt.close()
    
    print(f"\n[Success] Generated 6 professional visualizations in {fig_dir}/")

if __name__ == "__main__":
    visualize_rfm()
