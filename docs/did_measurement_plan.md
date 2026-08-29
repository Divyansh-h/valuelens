# Difference-in-Differences (DiD) Measurement Plan
**Campaign**: "Operation Hidden Gem" VIP Re-Engagement

To definitively prove the causal impact (incremental lift) of our VIP Re-Engagement campaign on the "Hidden Gem" customer segment, we will utilize a **Difference-in-Differences (DiD)** econometric framework. 

This approach isolates the true effect of the campaign by stripping out organic baseline changes (such as natural seasonality or overall macroeconomic trends) that affect both the Treatment and Control groups equally.

---

## 1. Experimental Cohorts
We rely on the randomized 80/20 A/B split of our 720 eligible customers:
- **Treatment Group (T):** ~576 customers who receive the £50 VIP credit.
- **Control Group (C):** ~144 customers who receive no intervention.

*Assumption: Because the groups are randomly assigned, their baseline behaviors and sensitivity to seasonality are statistically identical.*

## 2. Temporal Boundaries
We define two strict observation windows of equal length to ensure fair pre/post comparisons:
- **Pre-Period (t = 0):** The 60 days immediately *prior* to the campaign launch date.
- **Post-Period (t = 1):** The 60 days immediately *following* the campaign launch date.

## 3. The Core Metric
Our primary measurable variable is **Total Customer Spend (Revenue)** within the observation window.

Let $Y$ represent the total spend for a given customer group in a given period. We will calculate the average spend per customer in four states:
1. $Y_{T, 0}$: Average spend in Treatment Group, Pre-Period.
2. $Y_{T, 1}$: Average spend in Treatment Group, Post-Period.
3. $Y_{C, 0}$: Average spend in Control Group, Pre-Period.
4. $Y_{C, 1}$: Average spend in Control Group, Post-Period.

---

## 4. The Difference-in-Differences Calculation

To find the true incremental lift (the "DiD Estimator" or $\delta$), we calculate the change over time for the Treatment group, and subtract the organic change over time observed in the Control group.

### The Formula:
$$ \delta = (Y_{T, 1} - Y_{T, 0}) - (Y_{C, 1} - Y_{C, 0}) $$

### Why this matters:
If the Treatment group's average spend increases by £100 in the Post-Period, a naive analysis would claim the campaign generated £100 in value per customer. However, if the Control group's average spend organically increased by £20 in the exact same time period (due to natural seasonality, like Black Friday), the *true* causal impact of our campaign is only **£80**. The DiD framework prevents us from over-reporting campaign ROI.

## 5. Statistical Significance Verification
To ensure the observed lift $\delta$ is not simply due to random variance, we will fit an Ordinary Least Squares (OLS) regression model to the customer-level data:

$$ Y_{i,t} = \beta_0 + \beta_1(Treatment_i) + \beta_2(PostPeriod_t) + \beta_3(Treatment_i \times PostPeriod_t) + \epsilon_{i,t} $$

- $\beta_3$ represents our DiD estimator (the true incremental lift).
- If the p-value for $\beta_3$ is **< 0.05**, we can confidently reject the null hypothesis and state with 95% confidence that the VIP Re-Engagement campaign successfully caused a statistically significant increase in customer spend.
