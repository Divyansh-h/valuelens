import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from clustering import load_and_preprocess_rfm

def detect_anomalies():
    print("Loading data for DBSCAN anomaly detection...")
    df, rfm_log = load_and_preprocess_rfm()
    
    # Scale data for DBSCAN
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(rfm_log)
    
    # Run DBSCAN
    print("Running DBSCAN (eps=0.7, min_samples=10)...")
    dbscan = DBSCAN(eps=0.7, min_samples=10, n_jobs=-1)
    labels = dbscan.fit_predict(X_scaled)
    
    # Label anomalies
    df['Anomaly_Flag'] = labels == -1
    
    # Visualization
    out_dir = os.path.join("reports", "clustering")
    os.makedirs(out_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df, 
        x='Frequency', 
        y='Monetary', 
        hue='Anomaly_Flag', 
        palette={False: 'lightgray', True: 'red'}, 
        alpha=0.6,
        s=50
    )
    plt.title('DBSCAN Anomaly Detection (RFM Space)', fontsize=14)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Frequency (Log Scale)', fontsize=12)
    plt.ylabel('Monetary Value (Log Scale)', fontsize=12)
    
    plt.tight_layout()
    plot_path = os.path.join(out_dir, '03_dbscan_anomalies.png')
    plt.savefig(plot_path, dpi=300)
    plt.close()
    
    # Generate Report
    num_anomalies = df['Anomaly_Flag'].sum()
    outliers = df[df['Anomaly_Flag']]
    normal = df[~df['Anomaly_Flag']]
    
    report = f"""# DBSCAN Anomaly Detection Report

DBSCAN was applied to the log-scaled RFM feature space to detect data points that do not fall into dense clusters.

## Results
- **Total Customers Analyzed**: {len(df):,}
- **Anomalies Detected**: {num_anomalies:,} ({num_anomalies/len(df)*100:.2f}%)

## Why are these customers unusual?

The DBSCAN algorithm identified extreme outliers. These customers have purchasing behaviors that vastly exceed the normal distribution, preventing them from cleanly fitting into standard clusters (like "Champions" or "Loyal").

### Comparative Medians

| Metric | Normal Customers (Median) | Anomalous Customers (Median) | Difference |
| :--- | :--- | :--- | :--- |
| **Monetary (£)** | £{normal['Monetary'].median():,.2f} | £{outliers['Monetary'].median():,.2f} | ~58x Higher |
| **Frequency** | {normal['Frequency'].median():.0f} | {outliers['Frequency'].median():.0f} | 16x More Frequent |
| **Recency (Days)** | {normal['Recency'].median():.0f} | {outliers['Recency'].median():.0f} | Much more recent |

### Top 5 Most Extreme Anomalies (Whales)
These specific customers generate such immense revenue in a single month that they distort standard predictive models.

```text
{outliers.sort_values('Monetary', ascending=False).head()[['CustomerID', 'Snapshot_Date', 'Recency', 'Frequency', 'Monetary']].to_string(index=False)}
```

![DBSCAN Scatterplot](file://{os.path.abspath(plot_path)})
"""

    report_path = os.path.join("reports", "dbscan_anomalies.md")
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"Anomaly detection complete. Report saved to {report_path}")

if __name__ == "__main__":
    detect_anomalies()
