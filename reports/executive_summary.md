# ValueLens: One-Page Executive Summary

**Business Problem: What problem are we solving?**
The business currently lacks a data-driven understanding of customer value, churn risk, and revenue exposure. This results in inefficient "spray-and-pray" marketing, where margin-killing discounts are wasted on VIPs who would buy at full price, and retargeting ad budgets are wasted on dead accounts, severely damaging Return on Ad Spend (ROAS).

**Key Finding: What did the customer data reveal?**
The business suffers from extreme revenue concentration. Out of 3,917 total customers generating £7.24M in revenue, the **Top 10% of customers are responsible for roughly 72% of all lifetime revenue.** Conversely, our machine learning and RFM models discovered that 25% of the entire customer base (the "Lost" segment) accounts for just 5.3% of revenue, having only purchased ~1 time before churning completely.

**Customer Risk: Which customers are most at risk?**
The highest point of financial exposure is the **"At Risk (High Value)"** segment. Consisting of 266 customers (£545k total revenue exposure), these are historically strong buyers with a median lifetime spend of £1,361 (which is actually *higher* than the active "Loyal Customer" tier). However, their engagement has severely decayed, averaging 129 days since their last transaction. They are on the precipice of permanent churn.

**Revenue Opportunity: Where is the largest actionable opportunity?**
Rescuing the "At Risk" segment is the single highest-ROI opportunity for the business. Based on scenario modeling using their historical Average Order Value (AOV), even a highly pessimistic **5% reactivation rate** (triggering just 13 transactions) yields an estimated **£4,459** in rescued top-line revenue (at a median AOV of £343). Because these customers have proven buying habits, the Customer Acquisition Cost (CAC) to win them back is mathematically far lower than acquiring 13 new customers on the open market.

**Recommendation: What should the business do?**
Immediately reallocate active marketing budget away from the "Lost" segment (dormant >6 months) and deploy it entirely into a targeted, aggressive win-back campaign aimed exclusively at the 266 "At Risk" customers. Because of their high historical lifetime value, it is financially viable to use deep discounts (e.g., 30% off) or expensive human labor (account manager phone calls) to trigger a single transaction and reset their Recency clock.

**Measurement: How should success be measured?**
Success must be measured via a formal A/B Test utilizing a pure Control Group to calculate **Incremental Revenue per Customer**. Judging the campaign by "Total Revenue Generated" is analytically flawed because it fails to account for the baseline organic reactivation rate, meaning the business could accidentally claim credit for revenue that would have occurred anyway. 

**Limitation: What can this analysis NOT tell us?**
This analysis relies on a **point-in-time, cross-sectional snapshot**. While it perfectly identifies current financial exposure, the dataset cannot mathematically prove *longitudinal* transition rates (e.g., the exact probability that a new customer will become a Champion within 12 months). To track life-cycle movement probabilistically, the business must transition from a static snapshot to a recurring monthly reporting architecture.
