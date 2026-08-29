# Limitations: Correlation vs. Causation

When interpreting the findings from the ValueLens analytical pipeline (RFM Segmentation, K-Means Clustering, and CLV Predictions), it is absolutely critical for the marketing and leadership teams to understand the boundary between **Descriptive Correlation** and **Causal Inference**.

Failing to distinguish between the two can lead to massive misallocation of marketing budgets.

---

## 1. Descriptive & Correlational Findings (What We Know)
The vast majority of our analytical pipeline is descriptive. It accurately maps *what* happened and *who* did it, but it cannot prove *why* they did it.

*   **RFM Segments and K-Means Clusters:** 
    *   *Finding:* "Cluster 2 (Whales) accounts for 13% of customers but 57% of revenue."
    *   *Limitation:* This is a pure historical correlation. We do not know causally *why* they are whales. Did a specific marketing campaign create them? Do they only buy a specific premium product? The model only knows they spent heavily, not the catalyst.
*   **CLV Predictions (BG/NBD & Gamma-Gamma):**
    *   *Finding:* "We expect Customer X to spend £5,000 next year."
    *   *Limitation:* This is a probabilistic projection based on the assumption that the future will linearly resemble the past. If a competitor drops their prices by 50% tomorrow, this prediction will fail because the model does not causally understand market elasticity.
*   **The 'Hidden Gem' Mismatch:**
    *   *Finding:* "720 'Lost' customers are actually high-value."
    *   *Limitation:* This correlates historic spending velocity with future potential. It does not mean they *will* organically return. It simply flags that *if* they return, their baskets are statistically likely to be large. 

---

## 2. Causal Claims (What Requires an Experiment)
To move from observing data to actually pulling levers that predictably drive revenue, we must run controlled experiments. The following claims **cannot** be made without a rigorous, randomized A/B test (like the Difference-in-Differences design we drafted):

*   **"Sending a £50 discount to At-Risk customers will save the company £3.6 Million."**
    *   *Why we can't say this:* We have no causal proof that a £50 discount will successfully reactivate them. Furthermore, we don't know if the £50 discount will cannibalize organic revenue from customers who would have eventually returned anyway.
    *   *How to prove it:* Run a randomized controlled trial (RCT) with a strict holdout group to measure true incremental lift.
*   **"Our new loyalty program caused an increase in Champion-tier customers."**
    *   *Why we can't say this:* Natural seasonality (e.g., the holiday shopping season) might have driven the increase in frequency, completely independent of the loyalty program.
    *   *How to prove it:* Use a Difference-in-Differences (DiD) framework to subtract the organic baseline growth of a control group from the treatment group.
*   **"Customers in Cluster 1 churned because our shipping is too slow."**
    *   *Why we can't say this:* Unsupervised clustering models (like K-Means) do not have access to qualitative reasons. They only see the *result* (high recency, low frequency). 
    *   *How to prove it:* Cross-reference churn clusters with qualitative customer support tickets or post-churn surveys to establish a causal link.

## Summary
The current pipeline acts as a **highly sophisticated targeting radar**. It perfectly correlates past behavior to identify exactly *who* we should be looking at. However, discovering *what* action definitively changes their behavior requires strict, causal A/B testing.
