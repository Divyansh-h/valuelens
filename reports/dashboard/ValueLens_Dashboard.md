# ValueLens: Executive Analytics Dashboard

This dashboard is a lightweight, reproducible analytical report synthesized dynamically from the core ValueLens dataset.

## 1. Executive Summary (KPIs)

| Metric | Value |
| :--- | :--- |
| **Total Customers** | 3,917 |
| **Total Revenue** | £7,244,495.32 |
| **Avg Customer Value** | £1,849.50 |
| **Champions %** | 25.7% |
| **At Risk Revenue** | £545,169.87 |
| **Top 10% Revenue Share** | 59.6% |

---

## 2. Customer Segment Overview

We map our customer base across 5 heuristic behavioral segments based on Recency and Frequency.

![Segment Distribution](figures/01_segment_dist.png)

---

## 3. Revenue Contribution

While "Lost" customers dominate the headcount, the "Champions" segment holds the vast majority of financial value.

![Revenue by Segment](figures/02_segment_rev.png)

---

## 4. Revenue Concentration

The Lorenz curve demonstrates our exposure. The top 10% of customers generate nearly 60% of total revenue.

![Revenue Concentration](figures/04_revenue_concentration.png)

---

## 5. RFM Visualization

Visualizing the correlation between high Recency (low days) and massive Lifetime Spend (Log Scale).

![RFM Scatter](figures/03_rfm_scatter.png)

---

## 6. Retention Opportunity & Scenario Analysis

**Objective**: Rescue the "At Risk (High Value)" segment.
**Risk**: £545,170 in capital exposure.

The following model calculates the estimated top-line revenue recovered from a deep-discount win-back campaign, assuming it triggers a single transaction at the historical Median AOV of the segment. *(Note: This is a scenario analysis, not a guaranteed forecast).*

![Scenario Analysis](figures/05_scenario_analysis.png)
