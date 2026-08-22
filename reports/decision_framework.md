# ValueLens: Central Decision Science Framework

This document outlines the core Decision Science layer of the ValueLens project. It translates the analytical customer segmentation (RFM and K-Means) into an actionable, experiment-driven operational strategy. 

For each segment, we define the strategic objective, the recommended intervention, and a rigorous statistical experiment to validate the ROI of the decision.

---

## 1. At Risk (High Value)
**1. Business Objective:** Reactivation / Win-Back
**2. Customer Behavior:** Proven high lifetime spend and historical frequency, but their engagement has severely decayed (slipping Recency).
**3. Business Risk/Opportunity:** This is the highest point of financial exposure. If they are not reactivated immediately, all future recurring revenue is lost.
**4. Recommended Action:** Deploy aggressive, margin-heavy discounts or assign a dedicated account manager to trigger a single transaction (resetting the Recency clock).
**5. Suggested Communication Strategy:** "We Miss You" messaging paired with high urgency and an undeniable financial incentive.
**6. Priority:** CRITICAL
**7. KPI to Measure:** Reactivation Rate (%), Incremental Revenue Recovered (£).
**8. Validating Experiment:** 
* **Design:** A/B test an automated 30% deep-discount email (Treatment A) against personalized phone outreach from an account manager (Treatment B).
* **Hypothesis:** For B2B/Wholesale outliers, personal outreach will yield a statistically significantly higher reactivation rate than automated discounts, justifying the higher Customer Acquisition Cost (CAC) of human labor.

---

## 2. Loyal Customers
**1. Business Objective:** Value Maximization (Cross-Selling)
**2. Customer Behavior:** Consistent, steady repeat buyers with average/solid lifetime spend.
**3. Business Risk/Opportunity:** The business is leaving money on the table. Statistical testing proved that pushing a Loyal customer to the "Champion" tier yields a massive, statistically significant leap in lifetime revenue.
**4. Recommended Action:** Introduce product bundles, volume pricing tiers, and cross-category recommendations to increase Average Order Value (AOV).
**5. Suggested Communication Strategy:** Educational and complementary: *"Customers who bought X also loved Y."*
**6. Priority:** HIGH
**7. KPI to Measure:** Average Order Value (AOV), Cross-Category Penetration Rate.
**8. Validating Experiment:** 
* **Design:** A/B test a standard single-item promotional email (Control) against a bundled "Buy 2 Get 1 Free" offer (Treatment).
* **Hypothesis:** The bundled offer will generate a statistically significant lift in AOV compared to the standard promotion, proving the viability of volume-based upselling for this segment.

---

## 3. Champions
**1. Business Objective:** Retention & Brand Advocacy
**2. Customer Behavior:** Extreme leverage. They buy frequently, spend massively, and purchased very recently.
**3. Business Risk/Opportunity:** The primary risk is margin erosion from over-discounting customers who would have bought at full price anyway.
**4. Recommended Action:** Cease all financial discounts. Shift entirely to VIP treatment, early product access, and dedicated support queues to protect the baseline cash flow.
**5. Suggested Communication Strategy:** Exclusive and personalized: *"You're on the list for early access."*
**6. Priority:** MEDIUM-HIGH (Structural Defense)
**7. KPI to Measure:** Retention Rate (%), Margin Maintained (£).
**8. Validating Experiment:** 
* **Design:** Holdout Experiment. Suppress a random 10% of Champions from all promotional discount campaigns for 6 months (Control), while the remaining 90% receive normal discounts (Treatment).
* **Hypothesis:** The suppressed Control group will show no statistically significant drop in purchase frequency, proving that discounting this segment is wasted margin.

---

## 4. Potential Loyalists
**1. Business Objective:** Habit Formation
**2. Customer Behavior:** Very recent acquisitions, but have only made 1 or 2 purchases historically.
**3. Business Risk/Opportunity:** Very high early-churn risk. If they do not form a buying habit quickly, they will plummet into the "Lost" segment.
**4. Recommended Action:** Implement an automated onboarding series and trigger a specific incentive tied explicitly to completing a second purchase.
**5. Suggested Communication Strategy:** Brand storytelling paired with a "Welcome" incentive.
**6. Priority:** MEDIUM
**7. KPI to Measure:** Second-Purchase Conversion Rate, Time-to-Second-Purchase (Days).
**8. Validating Experiment:** 
* **Design:** A/B test the timing of the second-purchase incentive. Trigger the discount at Day 15 post-acquisition (Treatment A) versus Day 30 post-acquisition (Treatment B).
* **Hypothesis:** Triggering the incentive at Day 15 will result in a statistically significant lift in Second-Purchase Conversion Rate compared to Day 30, proving the necessity of rapid habit formation.

---

## 5. Lost
**1. Business Objective:** Cost Minimization (Capital Reallocation)
**2. Customer Behavior:** Total inactivity for 6+ months, coupled with historically low spend and frequency.
**3. Business Risk/Opportunity:** Wasting active marketing budget (ads, direct mail) on dead accounts, generating negative Return on Ad Spend (ROAS).
**4. Recommended Action:** Remove these customers from all paid retargeting lists. Retain them only on passive, zero-marginal-cost channels (like a monthly newsletter).
**5. Suggested Communication Strategy:** Zero active outreach.
**6. Priority:** LOWEST
**7. KPI to Measure:** Marketing Spend per Churned User (Target: £0).
**8. Validating Experiment:** 
* **Design:** Holdout suppression. Suppress 50% of the Lost segment from all paid marketing channels (Treatment) and leave 50% active in the paid retargeting pool (Control).
* **Hypothesis:** There will be no statistically significant difference in organic reactivation rates between the two groups, mathematically proving that the ad spend on the Control group was completely wasted.
