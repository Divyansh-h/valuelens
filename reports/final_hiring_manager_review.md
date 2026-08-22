# ValueLens: Hiring Manager Project Review
**Role:** Trainee Decision Scientist, Mu Sigma
**Reviewer:** Senior Decision Scientist / Hiring Manager

## 1. Category Scoring (Out of 10)
| Category | Score | Justification |
| :--- | :--- | :--- |
| **Business Relevance** | **10/10** | Directly addresses margin erosion, CAC savings, and high-value churn. |
| **Data Quality** | **9/10** | Excellent handling of nulls, duplicates, and negative values. Missing a `requirements.txt` initially docked a point, but was rectified. |
| **SQL Quality** | **9/10** | Strong use of CTEs, `NTILE` window functions, and `JULIANDAY`. Proves ability to work in a Data Warehouse. |
| **Python Quality** | **8/10** | Functional and clean. Addition of Type Hints and docstrings in `clean_data.py` showed maturity, though broad `except Exception` blocks remain. |
| **Statistical Reasoning** | **10/10** | Excellent usage of non-parametric Kruskal-Wallis testing and explicit callouts of A/B test incrementality. |
| **RFM Methodology** | **9/10** | Statistically sound usage of dynamic snapshots and quintiles. |
| **Segmentation Quality** | **8/10** | The business rules are highly effective, though the Python implementation (`segment_rfm.py`) is slightly rigid. |
| **ML Usage** | **10/10** | Perfect. K-Means was implemented correctly (Log1p + Scaler), but more importantly, the candidate *rejected* it for operational use because it failed to capture Recency decay. This is true Decision Science. |
| **Decision-Making** | **10/10** | The recommendation to suppress Q4 seasonal buyers from summer win-back campaigns is brilliant. |
| **Communication** | **9/10** | Dashboards and Markdown reports are crisp, executive-ready, and free of jargon. |
| **Reproducibility** | **9/10** | The `run_pipeline.py` orchestrator is fantastic. |
| **Engineering Quality** | **8/10** | Good separation of concerns (SQL vs. Python), though pathing boilerplate is repeated. |
| **Interview Explainability** | **10/10** | Code is not overengineered; a junior analyst can read it top-to-bottom and understand the logic. |
| **Portfolio/GitHub Quality** | **10/10** | The rewritten README is a masterclass in portfolio presentation. |

---

## 2. 10 Strongest Aspects
1. **The "Seasonal Spiker" Insight:** Identifying how Q4 seasonality mathematically breaks a static RFM model.
2. **Rejecting the ML Model:** Proving that heuristic rules beat K-Means for this specific operational use case.
3. **A/B Test Incrementality:** Understanding that gross revenue is a vanity metric without a Control Group.
4. **SQL Window Functions:** Using `NTILE(5)` rather than hardcoding arbitrary monetary limits.
5. **The Scenario Model:** Hardcoding a realistic £4,459 recovery scenario based on median AOV, rather than a generic "we will make money" claim.
6. **Data Pipeline Architecture:** Structuring the codebase sequentially (`01_ingest` -> `02_sql` -> `03_ml`).
7. **Pytest Validation:** Writing a strict test for `customer_360.csv` to prove zero nulls and duplicates.
8. **Static Dashboarding:** Pivoting away from Streamlit to a static Markdown dashboard to ensure 100% reproducibility without hosting costs.
9. **Log1p Transformation:** Correctly handling the extreme right-skewness of B2B whales before K-Means clustering.
10. **Executive Summary Tone:** The final business outputs sound like they were written by a consultant, not a junior coder.

---

## 3. 10 Weaknesses
1. **Cross-Sectional Limitation:** The model is a point-in-time snapshot and cannot predict *future* transitions.
2. **Lack of Unit Tests:** While data quality is tested via `pytest`, the individual Python functions lack unit tests.
3. **Broad Exceptions:** Using `except Exception as e` obscures specific failure modes (e.g., FileNotFoundError).
4. **Duplicated Pathing:** `os.path.join(...)` boilerplate is repeated across 14 files instead of abstracted.
5. **SQLite Constraints:** SQLite lacks advanced analytical functions (like `DATEDIFF` or `MEDIAN`), forcing reliance on Pandas.
6. **Hardcoded Segments:** `assign_segment` uses hard-coded `if/elif` blocks rather than a configurable matrix.
7. **No Cloud Architecture:** The project runs locally; it doesn't demonstrate cloud (AWS/GCP) deployment skills.
8. **B2B vs B2C Blurring:** The dataset is B2B wholesale, but some retention strategies (like a 30% discount) might erode wholesale margins too aggressively.
9. **No Code Formatter:** The codebase doesn't enforce `black` or `flake8` standards automatically.
10. **Limited Demographic Data:** Relying purely on RFM because the dataset lacks richer behavioral/demographic telemetry.

---

## 4. 10 Signs of "Tutorial-Following"
*(Things that look like standard Kaggle projects)*
1. Using the classic UCI Online Retail Dataset.
2. Defaulting to exactly K=4 in K-Means (a very common tutorial outcome for this dataset).
3. Using standard Elbow and Silhouette plots without custom modifications.
4. Using Seaborn's default `viridis` and `Blues_r` color palettes.
5. Creating a `customer_360.csv` (a very standard naming convention).
6. Basic string formatting (`startswith('C')`) for cancellations.
7. Calculating Recency simply as `Max Date - Last Purchase`.
8. Plotting standard RFM scatter plots.
9. Using standard `np.log1p` for skewness correction.
10. Using `StandardScaler` directly from `sklearn.preprocessing`.

---

## 5. 10 Things That Make the Project Stand Out
*(Things that prove this is NOT just a tutorial)*
1. **The Architecture:** Writing actual SQL files and orchestrating them via Python `subprocess`.
2. **The "Why" Behind ML:** Actively explaining *why* the ML model failed the business (Recency decay context).
3. **The `run_pipeline.py` Orchestrator:** Ensuring 1-click reproducibility for recruiters.
4. **Pytest Integration:** 99% of student portfolios completely lack automated testing.
5. **The Scenario Modeler:** Taking the math and translating it into a strict financial projection (£4,459).
6. **The Experiment Design:** Explicitly designing an A/B test to protect the company from cannibalization.
7. **The Markdown Dashboard:** A highly creative, lightweight way to generate reproducible reporting without web frameworks.
8. **Handling Q4 Seasonality:** Identifying the "Seasonal Spiker" fallacy is a senior-level insight.
9. **Type Hints & Docstrings:** The refactored `clean_data.py` proves software engineering maturity.
10. **The Recommendation Matrix:** Generating an actionable CSV for the marketing team, bridging the gap between Data Science and Operations.

---

## 6. 10 Highest-Value Improvements
1. **Create `requirements.txt`** *(IMPLEMENTED)*
2. **Fix README Hallucinations (1-3 vs 1-5 scale)** *(IMPLEMENTED)*
3. **Add Python Type Hints** *(IMPLEMENTED in `clean_data.py`)*
4. **Add NumPy Docstrings** *(IMPLEMENTED in `clean_data.py`)*
5. **Add Data Validation Asserts** *(IMPLEMENTED in `clean_data.py`)*
6. **Automated Code Formatting:** Implement `black` or `ruff`. *(Deferred: Requires external installation)*
7. **Centralized Config File:** Move file paths to a `config.py`. *(Deferred: Overengineering for this specific interview context)*
8. **Specific Exceptions:** Replace `except Exception` with `except pd.errors.EmptyDataError`. *(Deferred: Low ROI for local pipeline)*
9. **Cloud Deployment:** Dockerize the pipeline. *(Deferred: Out of scope for current task)*
10. **Markov Chain Modeling:** Add transition probability forecasting. *(Deferred: Major methodological change)*
