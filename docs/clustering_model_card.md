# Model Card: ValueLens RFM Customer Segmentation

## Model Details
- **Model Type**: Unsupervised Machine Learning (Clustering)
- **Primary Algorithm**: K-Means Clustering
- **Feature Space**: Recency, Frequency, Monetary (RFM)
- **Objective**: Segment the retail customer base into behaviorally cohesive, mathematically distinct groups to inform targeted marketing and retention strategies.

## Data Preprocessing & Scaling Strategy
Because K-Means utilizes Euclidean distance, it is highly sensitive to the scale and distribution of data. We applied a strict two-step preprocessing pipeline:
1. **Log Transformation**: A `log1p` transformation was applied to all raw RFM values to squash the extreme right-skewness of the retail data (particularly Monetary value).
2. **Standardization (Zero Data Leakage)**: The log-transformed data was scaled using `sklearn.preprocessing.StandardScaler`. Crucially, this scaler was wrapped inside a `sklearn.pipeline.Pipeline` and fitted *strictly* on an 80% training split. The remaining 20% (and full predictions) are routed through this fitted scaler to guarantee zero data leakage during algorithmic evaluation.

## Final K and Justification
- **Final Selected K**: `4`
- **Algorithmic Justification**: We evaluated $K \in [2, 10]$ using the Elbow Method (Inertia) and Silhouette Scores. While $K=2$ achieved the mathematical absolute maximum silhouette score (~0.428), $K=4$ exhibited a very strong secondary peak (~0.345) while aligning with the elbow of the inertia curve. 
- **Business Justification**: $K=4$ was ultimately chosen because it provides the necessary granularity for business operations. A 2-cluster solution merely splits the user base into "Good" and "Bad", whereas 4 clusters distinctly isolate "Whales", "Core/Loyal", "New/Recent", and "Churned". 

## Model Stability & Validation
To ensure the clusters capture true underlying market dynamics rather than overfitting to random noise, we conducted rigorous non-parametric testing:
- **Bootstrap Stability Testing**: We resampled the customer base with replacement 20 independent times and refitted the K-Means algorithm from scratch on each permutation. 
- **Adjusted Rand Index (ARI)**: The average ARI across all 20 iterations was an exceptional **0.9704** (where 1.0 is perfect stability). 
- **Conclusion**: The K-Means boundaries are **Extremely Stable** and highly robust to variance in the data.

### Algorithmic Comparisons
We compared our strict spherical K-Means boundaries against a probabilistic **Gaussian Mixture Model (GMM)** which allows for ellipsoidal covariance. The Adjusted Rand Index between the K-Means and GMM outputs was > 0.8, proving that the spherical assumptions of K-Means are entirely sufficient for this feature space. 

## Known Limitations
- **Extreme Whales (Anomalies)**: A secondary DBSCAN analysis detected exactly 46 massive outliers (0.14% of the customer base) who spend upwards of ~58x more than average customers. Because K-Means utilizes standard Euclidean distance, these massive outliers pull the centroids slightly outward. Future iterations may benefit from completely isolating these whales prior to K-Means fitting.
- **Temporal Drift**: RFM clustering represents a static snapshot of behavior. If macroeconomic conditions shift, the scaled boundaries will become stale. The model must be periodically retrained (e.g., quarterly) to adjust its moving averages and standardizations.
- **Lack of Product Affinity**: This model purely segments users on generic transaction volume (RFM), meaning it has zero awareness of *what* products they are actually buying.
