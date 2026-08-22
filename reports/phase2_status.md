# ValueLens: Phase 2 Status Report

## Audit Summary
A comprehensive audit of Phase 2 (RFM Analytics & Customer Segmentation) was conducted. All data engineering logic, SQL calculations, and visualization engines were independently verified. 

- **SQL Implementation**: The SQLite CTE safely calculated Recency using a deterministic snapshot date (`MAX(date) + 1 day`). `NTILE(5)` sorting was verified for accuracy (e.g., `ORDER BY recency_days DESC` successfully assigned the highest score to the most recent customers).
- **Validation**: 14/14 automated tests passed, confirming data bounds (Recency >= 0, Frequency >= 1, Monetary > 0, Scores 1-5) and independently recalculating RFM logic via Pandas to verify the SQL results perfectly.
- **Reporting Integrity**: All aggregated statistics, percentages, and segment counts in the markdown reports were confirmed to be dynamically calculated directly from the `customer_rfm.csv` dataset, not manually hardcoded.
- **Visualizations**: All 7 charts were generated successfully using accurate scaling (Log10 where appropriate) and saved natively as high-resolution PNGs.

---

## Top 10 Analytical Findings

Based on the quantitative outputs of the RFM calculation, the heuristic segmentation rules, and the Lorenz curve concentration analysis, here are the 10 most critical business insights discovered:

1. **Clean Baseline**: The active UK cohort consists of exactly 3,917 uniquely identified customers driving £7.24M in total revenue across 16,590 distinct orders.
2. **Extreme Skewness**: The behavioral data exhibits massive right-skewness in both Frequency (skew: 10.63) and Monetary value (skew: 20.46), primarily driven by a handful of extreme B2B wholesale outliers (max spend: £259k).
3. **The Average vs. Median Trap**: Because of this extreme skew, "Average Customer Spend" is a dangerous metric for forecasting. The median spend is consistently less than half of the arithmetic mean across high-value tiers.
4. **The 1% "Whale" Dependency**: A microscopic fraction of the base—the Top 1% of customers—is responsible for generating an astonishing **29.3%** of all revenue.
5. **The Extreme Pareto Effect**: The dataset strictly follows an aggressive 80/20 rule, with the top 20% of the customer base driving **73.3%** of the company's total revenue.
6. **The Irrelevant Bottom Half**: Conversely, the bottom 50% of all acquired customers contribute a mathematically negligible **8.3%** of total revenue, suggesting broad-based acquisition marketing is highly inefficient.
7. **Champion Dominance**: The "Champions" segment makes up just 25.7% of the total customer base (1,008 customers), yet it drives the vast majority of the cash flow (£4.72M, or 65.2% of total revenue).
8. **The Cost of Churn**: The "Lost" segment accounts for a full 25.0% of the customer base (981 customers) but contributes only 5.3% of revenue (£385k). Reactivating these customers is mathematically not worth the marketing spend.
9. **The Urgent Retention Target**: The "At Risk" segment comprises only 6.8% of the customer base, but represents £545k in capital exposure. Because these are historical high-spenders whose recency is slipping, they represent the single most urgent target for proactive retention campaigns.
10. **The Next Step (Algorithmic Modeling)**: The hard thresholds of our heuristic rules effectively separated the base, but they force continuous variables into arbitrary discrete buckets. The high skewness mathematically justifies moving to an algorithmic clustering model (like K-Means with Log transformation) in Phase 3 to find natural behavioral boundaries.
