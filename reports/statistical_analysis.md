# ValueLens: Statistical Analysis of RFM Segments

This report provides a deeper statistical analysis of the behavioral distributions within our heuristic customer segments. The goal is to determine if our high-level business rules (`R` and `F` thresholds) naturally created statistically significant, distinct financial outcomes (Monetary value) without explicitly hardcoding them.

## 1. Descriptive Statistics (Distribution Profiles)

### Recency (Days Since Last Purchase)
| Segment | Min | Median (50%) | Mean | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Champions** | 1.0 | 11.0 | 12.9 | 33.0 |
| **Loyal Customers** | 1.0 | 39.0 | 37.6 | 71.0 |
| **At Risk (High Value)** | 72.0 | 108.0 | 129.9 | 372.0 |
| **Potential Loyalist** | 1.0 | 53.0 | 80.6 | 360.0 |
| **Lost** | 71.0 | 218.0 | 216.8 | 374.0 |

*Interpretation:* The rules cleanly separated Recency. Champions buy within ~2 weeks. Lost customers haven't bought in over 7 months (218 days median).

### Frequency (Total Invoices)
| Segment | Min | Median (50%) | Mean | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Champions** | 3.0 | 7.0 | 9.9 | 206.0 |
| **At Risk (High Value)** | 3.0 | 4.0 | 4.9 | 34.0 |
| **Loyal Customers** | 2.0 | 3.0 | 3.6 | 62.0 |
| **Potential Loyalist** | 1.0 | 1.0 | 1.6 | 3.0 |
| **Lost** | 1.0 | 1.0 | 1.1 | 2.0 |

*Interpretation:* Frequency is extremely right-skewed. While the median Champion buys 7 times, the maximum is 206 times (Wholesale). The bottom tiers (Lost, Potential Loyalist) rarely exceed 1-2 purchases.

### Monetary (Lifetime Spend)
| Segment | Median (50%) | Mean | 75th Percentile | Max |
| :--- | :--- | :--- | :--- | :--- |
| **Champions** | £2,159.05 | £4,683.74 | £4,092.14 | £259,657.30 |
| **At Risk (High Value)** | £1,361.12 | £2,049.51 | £2,110.63 | £44,534.30 |
| **Loyal Customers** | £786.68 | £1,573.76 | £1,504.48 | £168,472.50 |
| **Potential Loyalist** | £345.97 | £446.95 | £594.45 | £4,459.52 |
| **Lost** | £241.06 | £393.14 | £350.06 | £77,183.60 |

*Interpretation:* Notice that "At Risk" customers actually have a *higher* median lifetime spend (£1,361) than active "Loyal Customers" (£786). This validates why they are explicitly labeled "(High Value)" and deserve a dedicated retention budget. 

---

## 2. Meaningful Statistical Testing

*Context: We segmented our customers strictly based on Recency and Frequency scores. We did not use Monetary value in our business rules. Therefore, a highly useful business question is: **Did targeting High Recency and High Frequency naturally isolate customers who spend significantly more money?***

### Test Assumptions & Selection
Traditional ANOVA requires the data to be normally distributed. As proven earlier, our Monetary data has a massive positive skew (20.46) driven by wholesale outliers. Using an arithmetic mean-based test like ANOVA would be statistically invalid. 

Instead, we use **Non-Parametric Tests** (which compare medians/ranks rather than means) to robustly handle the extreme outliers without requiring data transformation.

### Test A: Kruskal-Wallis H-Test (All Segments)
This tests the null hypothesis that the median Monetary spend is identical across all five segments.
- **H-Statistic**: `2484.93`
- **P-Value**: `0.00`
- **Result**: The null hypothesis is resoundingly rejected. The segments represent mathematically distinct populations of lifetime spend.

### Test B: Mann-Whitney U Test (Champions vs. Loyal Customers)
This tests the specific hypothesis that "Champions" spend significantly more money than "Loyal Customers", despite both groups being active, repeat buyers.
- **U-Statistic**: `612,154.50`
- **P-Value**: `2.90e-107`
- **Result**: The null hypothesis is rejected.

### Business Decision Usefulness
The Mann-Whitney U test mathematically proves that pushing a "Loyal Customer" (Median spend: £786) across the threshold to become a "Champion" (Median spend: £2,159) results in a statistically significant, massive leap in lifetime revenue. 

Therefore, marketing campaigns designed to cross-sell or increase purchase frequency for the "Loyal" tier have a proven, quantifiable ROI attached to them, entirely validating the RFM heuristic model.
