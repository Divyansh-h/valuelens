# ValueLens: K-Means Cluster Selection (K)

Before executing the final clustering model, we evaluated candidate values for K ranging from 2 through 8 using both the **Elbow Method (Inertia)** and **Silhouette Score**.

## Evaluation Metrics

| K | Inertia (WCSS) | Silhouette Score |
|---|----------------|------------------|
| 2 | 5806.13        | 0.4352           |
| 3 | 4333.48        | 0.3416           |
| **4** | **3500.34**    | **0.3394**       |
| 5 | 2926.89        | 0.3187           |
| 6 | 2530.50        | 0.3156           |
| 7 | 2254.04        | 0.3111           |
| 8 | 2064.34        | 0.3036           |

## Analytical Decision: Selecting K = 4

If we blindly follow the mathematical maximum Silhouette Score, we would select **K = 2** (Score: 0.4352). However, from a business perspective, clustering customers into just two groups (essentially "Good" vs "Bad") is far too broad to generate actionable, targeted marketing campaigns.

Looking at the curve, there is an "elbow" around K=3 and K=4. 
Crucially, the drop in Silhouette Score from K=3 to K=4 is extremely marginal (0.3416 → 0.3394, a negligible drop of ~0.002), but the Inertia (Within-Cluster Sum of Squares) drops significantly from 4333 to 3500. This indicates that moving from 3 to 4 clusters tighter, more mathematically cohesive groups without muddying the boundaries.

**Business Interpretability:**
Choosing **K = 4** offers the perfect balance between mathematical rigor and business utility. Four distinct algorithmic clusters will allow us to beautifully compare against our 5 heuristic segments (perhaps the algorithm naturally combines the "Lost" and "Potential Loyalist" groups, or isolates the "Champions" distinctly). 

Therefore, **K = 4** will be used for the final model generation.
