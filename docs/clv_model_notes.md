# Customer Lifetime Value (CLV) Model Notes

This document outlines the core mathematical assumptions, behavioral logic, and known limitations of the Beta-Geometric/Negative Binomial Distribution (BG/NBD) and Gamma-Gamma predictive models used in the ValueLens CLV pipeline.

---

## 1. Beta-Geometric / NBD (BG/NBD) Model
The BG/NBD model is used to predict **how many future transactions** a customer will make while they remain "alive" (active).

### Key Assumptions
* **Independent and Identically Distributed (i.i.d.) Transactions:** While a customer is active, the number of transactions they make in a given time period follows a Poisson distribution with a transaction rate $\lambda$. This assumes their purchasing rhythm is relatively steady.
* **Heterogeneity in Transaction Rates:** Transaction rates vary across the customer base. This variation is modeled using a Gamma distribution (parameters $r$ and $\alpha$).
* **Dropout After Purchase:** A customer has a probability $p$ of permanently "dropping out" or becoming inactive *immediately after* any given purchase. They do not drop out between purchases. 
* **Heterogeneity in Dropout Probability:** The dropout probability $p$ varies across customers according to a Beta distribution (parameters $a$ and $b$).
* **Independence of Rates:** The transaction rate $\lambda$ and dropout probability $p$ are completely independent of each other across customers.

### Limitations
* **No Seasonality Modeling:** The base BG/NBD model assumes a constant transaction rate $\lambda$ and does not account for macroeconomic seasonality (e.g., Q4 holiday spikes). If seasonality dominates the business, the predictions may misalign during off-peak months.
* **Ignores Churn Between Purchases:** The mathematical construct assumes a user can only "churn" immediately after checking out. In subscription businesses, churn happens on a calendar date regardless of purchasing. (Therefore, BG/NBD is strictly designed for *non-contractual* retail settings).

---

## 2. Gamma-Gamma Model
The Gamma-Gamma model is layered on top of the BG/NBD outputs to predict the **expected monetary value** of each future transaction.

### Key Assumptions
* **Independence of Frequency and Value (CRITICAL):** The model strictly assumes that the average monetary value of a customer's transaction is completely independent of their purchase frequency. (In our ValueLens dataset, we verified this via a Pearson correlation of $0.16$, satisfying the assumption).
* **Gamma Distributed Transaction Value:** The monetary value of a given customer's transactions varies randomly around their unobserved mean transaction value, following a Gamma distribution.
* **Heterogeneity in Mean Value:** The unobserved mean transaction values vary across the customer base, also following a Gamma distribution (parameters $p$, $q$, $v$).

### Limitations
* **Requires Repeat-Purchase Behavior:** The Gamma-Gamma model *cannot* calculate variance or heterogeneity for customers who have only purchased exactly once. It relies entirely on customers with 2+ purchases to infer the baseline monetary distributions. New or "one-and-done" customers simply inherit the population average.
* **Static Snapshot:** Just like BG/NBD, the Gamma-Gamma model does not inherently understand inflation or changing product pricing over time. It models historic spend capabilities.

---

## 3. General Pipeline Limitations
* **Product Agnostic:** The CLV pipeline models sheer transaction volume and gross spend. It has no awareness of *what* products the user buys, the profit margins of those specific products, or product lifecycle obsolescence.
* **Requires Periodic Retraining:** Because it does not model macroeconomic drift (like recessions) or aggressive new marketing campaigns, the model weights must be periodically re-calibrated (e.g., quarterly) against fresh transaction data to remain accurate.
