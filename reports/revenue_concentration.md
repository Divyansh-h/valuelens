# ValueLens: Customer Concentration & Revenue Exposure Analysis

This report examines the degree to which our business relies on a small fraction of high-value customers. By mapping the concentration of revenue generation, we can quantify financial exposure risks without making unsupported causal claims about behavior.

## Revenue Concentration Metrics

When ranking the entire customer base (3,917 customers) strictly by their total lifetime spend:

- **Top 1% of Customers** generate **29.3%** of total revenue.
- **Top 5% of Customers** generate **48.1%** of total revenue.
- **Top 10% of Customers** generate **59.6%** of total revenue.
- **Top 20% of Customers** generate **73.3%** of total revenue.
- **Bottom 50% of Customers** generate only **8.3%** of total revenue.

*(A cumulative concentration curve visualizing this distribution has been saved to `reports/figures/07_cumulative_revenue_curve.png`)*

## Financial Exposure by Critical Segments

Examining our previously defined heuristic segments reveals how much actual capital is tied up in different behavioral states:

- **Champions Exposure**: **£4,721,205.81** (65.2% of total revenue). 
  *Interpretation:* The business is highly leveraged on this segment. Retaining these specific accounts is structurally more important than acquiring new average customers.
- **At Risk Exposure**: **£545,169.87** (7.5% of total revenue). 
  *Interpretation:* This represents significant capital that historically flowed into the business but is currently dormant based on recent purchasing behavior. This quantifies the exact financial urgency of a win-back campaign.
- **Lost Capital**: **£385,671.48** (5.3% of total revenue). 
  *Interpretation:* Despite this group making up exactly 25.0% of the total headcount, the financial footprint of these permanently inactive, low-value customers is minimal.

## Analytical Interpretation

The concentration curve highlights extreme business leverage. While the standard Pareto principle suggests 20% of customers drive 80% of revenue, our concentration sits at **73.3%** at the 20% mark, demonstrating significant structural skew even beyond traditional retail assumptions. 

The primary vulnerability of the business model is customer churn at the very top of the distribution. The loss of a single "Top 1%" buyer (which includes our massive wholesale accounts) statistically offsets the acquisition of hundreds of median-value retail consumers. Thus, retention strategies targeting the "At Risk" segment and loyalty programs for "Champions" are inherently more protective of topline revenue than broad, generalized acquisition campaigns aimed at filling the bottom 50%.
