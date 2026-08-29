# DBSCAN Anomaly Detection Report

DBSCAN was applied to the log-scaled RFM feature space to detect data points that do not fall into dense clusters.

## Results
- **Total Customers Analyzed**: 33,262
- **Anomalies Detected**: 46 (0.14%)

## Why are these customers unusual?

The DBSCAN algorithm identified extreme outliers. These customers have purchasing behaviors that vastly exceed the normal distribution, preventing them from cleanly fitting into standard clusters (like "Champions" or "Loyal").

### Comparative Medians

| Metric | Normal Customers (Median) | Anomalous Customers (Median) | Difference |
| :--- | :--- | :--- | :--- |
| **Monetary (£)** | £497.65 | £29,243.62 | ~58x Higher |
| **Frequency** | 2 | 32 | 16x More Frequent |
| **Recency (Days)** | 49 | 18 | Much more recent |

### Top 5 Most Extreme Anomalies (Whales)
These specific customers generate such immense revenue in a single month that they distort standard predictive models.

```text
 CustomerID Snapshot_Date  Recency  Frequency  Monetary
      18102    2011-12-31       21         60 259657.30
      18102    2011-11-30        1         57 248171.76
      18102    2011-10-31        9         51 232840.68
      17450    2011-12-31       29         46 194390.79
      17450    2011-11-30        0         45 192828.39
```

![DBSCAN Scatterplot](file:///Users/divyansh/code/musigma/ValueLens/reports/clustering/03_dbscan_anomalies.png)
