# ValueLens: A/B Testing Framework (Retention Strategy)

To practically execute our Decision Science recommendations, we must validate our assumptions using a statistically rigorous A/B test. We will focus our experimental design on the highest-priority business objective: rescuing the **"At Risk (High Value)"** segment.

## The Flaw of "Revenue Generated"
Before designing the test, we must address the most common mistake in marketing analytics: judging a campaign by "Revenue Generated" alone. 

If we send a 30% discount email to the At Risk segment and they subsequently generate £10,000, it is dangerously tempting to claim the campaign was a success. However, without a control group, we cannot measure the **baseline organic reactivation rate**. What if those customers were going to buy anyway, and would have generated £9,500 *without* the discount? If that were true, the campaign actually destroyed margin and cannibalized organic revenue. 

Therefore, our experiment must be designed to measure **Incrementality** using a strict Control group.

---

## Experimental Design: The Win-Back Campaign

### 1. Allocation & Randomization
* **Target Audience:** The 266 customers currently flagged in the "At Risk (High Value)" segment.
* **Randomization Unit:** `CustomerID`. (Randomizing at the account level ensures that a customer receives consistent messaging across all channels and sessions).
* **Treatment Group (50%):** Receives the aggressive Win-Back campaign (e.g., an automated email sequence offering 30% off their next invoice).
* **Control Group (50%):** Receives "Business As Usual" (BAU) messaging, meaning no special discounts or active outreach.

### 2. Core Metrics
* **Primary KPI:** **Incremental Revenue per Customer**. (Average revenue in the Treatment group minus average revenue in the Control group). 
* **Secondary KPIs:** 
  * **Reactivation Rate (%)**: The percentage of customers who complete at least one transaction during the experiment.
  * **Offer Redemption Rate (%)**: To measure the operational friction/appeal of the specific discount code.
  * **Average Order Value (AOV)**: To verify if the deep discount artificially lowered transaction sizes.
* **Guardrail Metrics:** 
  * **Gross Margin %**: To ensure we are not buying top-line revenue at a negative net margin.
  * **Email Unsubscribe Rate**: To ensure the aggressive campaign is not permanently burning our communication channel with high-value accounts.

### 3. Parameters & Success
* **Experiment Duration:** 30 Days. (This provides a sufficiently long observation window for wholesale/B2B buyers to approve budgets and process a transaction, while remaining short enough to iterate).
* **Potential Confounders:** 
  * *Seasonality*: Testing during a major holiday or industry peak season might artificially inflate the reactivation rate across both groups, making it harder to detect the true treatment effect.
  * *Sales Rep Interference*: If human sales reps have access to the customer list, they might manually reach out to Control group customers, breaking the isolation of the experiment.
* **Success Criterion:** The Treatment group must generate a statistically significant lift (e.g., $p < 0.05$) in **Incremental Revenue** that strictly exceeds the cost of the 30% margin giveaway. If the lift is positive but fails to offset the discount cost, the test fails, and the strategy must be redesigned.
