# ValueLens: Portfolio Walkthrough Narration Script

**Target Duration:** ~2.5 - 3 Minutes  
**Pacing:** Confident, professional, avoiding overly dense jargon while highlighting business impact.

---

### [0:00 - 0:30] Introduction & Problem Statement
*(Screen showing the GitHub Repository README / Architecture Diagram)*

**Narrator:**
"Welcome to ValueLens. This is an end-to-end Machine Learning pipeline designed to solve a massive problem in retail and B2B: *spray-and-pray marketing*. 

Most companies rely on static, backward-looking heuristics—like basic Recency and Frequency scores—to decide who gets a discount. The problem? That approach actively misallocates marketing budgets. It accidentally gives discounts to VIPs who would have bought at full price, while burning retargeting cash on permanently churned accounts. 

ValueLens solves this by replacing static rules with probabilistic Machine Learning to predict exact future Customer Lifetime Value, protecting gross margin and maximizing ROI."

---

### [0:30 - 1:15] The Data Engineering & Pipeline
*(Screen: Open terminal, type `make run-pipeline` and hit enter. Show the structured logs streaming in real-time.)*

**Narrator:**
"The entire system is completely reproducible. By simply running `make run-pipeline`, we kick off a 17-stage orchestrated workflow. 

It starts by ingesting the UCI Online Retail dataset—over half a million rows of transaction data. We run a rigorous automated Data Quality Audit to catch duplicate transactions and negative prices. 

Then, the data is pushed into a local SQLite data warehouse. We use SQL to rapidly extract longitudinal behavioral features, taking advantage of database optimization before passing the clean data back to Python for machine learning."

---

### [1:15 - 2:00] The Machine Learning Models
*(Screen: Show the `RFMSegmenter.py` code briefly, then show the `predict_clv_bootstrap.py` terminal output with confidence intervals.)*

**Narrator:**
"For the analytics, we don't just stop at basic clustering. 

While we do use Unsupervised K-Means clustering to validate our customer segments, the real engine of ValueLens is the probabilistic modeling. We implemented the BetaGeo (BG/NBD) and Gamma-Gamma models from the lifetimes package. 

Instead of guessing if a customer is 'Lost', this model mathematically calculates their exact probability of being 'alive', and forecasts their expected spend over the next 12 months. We even run a 100-iteration Bootstrap simulation to generate 90% Confidence Intervals for every single customer's future value, quantifying our uncertainty for business stakeholders."

---

### [2:00 - 2:40] The Dashboard & Business Findings
*(Screen: Launch Streamlit via `make dashboard`. Show the Interactive Dashboard, filter for the "Hidden Gems", and show the Revenue Concentration Pareto chart.)*

**Narrator:**
"All of this complex math is surfaced to marketing teams via an interactive Streamlit dashboard. 

Here is our biggest finding: Static rules labeled a huge portion of our database as 'Lost' or 'At Risk'. But our probabilistic model identified exactly 720 of these customers as 'Hidden Gems' who actually belong in the top 25% of future revenue generators. 

If marketing blindly followed the legacy rules, they would abandon these customers, risking £3.7 Million in highly probable future revenue. Now, we can deploy a targeted win-back campaign exclusively for them."

---

### [2:40 - 3:00] Conclusion & DevOps
*(Screen: Show the GitHub Actions CI passing, or run `make test` in the terminal to show pytest passing.)*

**Narrator:**
"Finally, this isn't just a research notebook. It's production-ready. We've built an automated Pytest suite testing synthetic data, and a GitHub Actions Continuous Integration pipeline that runs on every commit to ensure no one breaks the ML logic. 

ValueLens isn't just about cool data science; it's a rigorously tested, automated decision engine built to drive measurable revenue."
