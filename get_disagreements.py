import pandas as pd
import os

csv_path = os.path.join("data", "processed", "customer_rfm.csv")
df = pd.read_csv(csv_path)

# Find 5 customers who are heuristically "Lost" (usually very bad) but clustered into Cluster 0 (usually high value/loyal)
disagreements = df[(df['Segment'] == 'Lost') & (df['Cluster'] == 'Cluster 0')]
print("\n--- Disagreement: Heuristic 'Lost' but K-Means 'Cluster 0' ---")
print(disagreements[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Segment', 'Cluster', 'RFM_Score']].head(5))

# Find 5 customers who are heuristically "Champions" but clustered into Cluster 1 (mostly lost/low value)
disagreements2 = df[(df['Segment'] == 'Champions') & (df['Cluster'] == 'Cluster 1')]
print("\n--- Disagreement: Heuristic 'Champions' but K-Means 'Cluster 1' ---")
print(disagreements2[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Segment', 'Cluster', 'RFM_Score']].head(5))
