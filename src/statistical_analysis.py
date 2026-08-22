import pandas as pd
import numpy as np
import os
import sys
from scipy import stats

def run_stats():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed", "customer_rfm.csv")
    df = pd.read_csv(csv_path)
    
    # Descriptive Stats by Segment for all three RFM variables
    print("--- Descriptive Stats (Recency) ---")
    print(df.groupby('Segment')['Recency'].describe().round(1))
    
    print("\n--- Descriptive Stats (Frequency) ---")
    print(df.groupby('Segment')['Frequency'].describe().round(1))
    
    print("\n--- Descriptive Stats (Monetary) ---")
    print(df.groupby('Segment')['Monetary'].describe().round(2))
    
    # Statistical Testing
    # We segmented customers based ONLY on Recency and Frequency scores.
    # The most useful question: Did isolating High R & High F naturally isolate High Monetary value?
    
    print("\n--- Statistical Testing (Monetary Value Separation) ---")
    
    # Kruskal-Wallis H-Test
    groups = [group['Monetary'].values for name, group in df.groupby('Segment')]
    kw_stat, kw_p = stats.kruskal(*groups)
    print("Kruskal-Wallis H-Test across all segments:")
    print(f"H-Statistic: {kw_stat:.2f}")
    print(f"P-Value: {kw_p:.2e}")
    
    # Mann-Whitney U Test (Champions vs Loyal)
    champs = df[df['Segment'] == 'Champions']['Monetary']
    loyal = df[df['Segment'] == 'Loyal Customers']['Monetary']
    
    mw_stat, mw_p = stats.mannwhitneyu(champs, loyal, alternative='greater')
    print("\nMann-Whitney U Test (Champions Spend > Loyal Customers):")
    print(f"U-Statistic: {mw_stat:.2f}")
    print(f"P-Value: {mw_p:.2e}")

if __name__ == "__main__":
    run_stats()
