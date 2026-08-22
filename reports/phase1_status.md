# ValueLens: Phase 1 Status Report

## What Was Built
- **Project Structure**: Created a modular, professional directory layout (`data`, `database`, `notebooks`, `presentation`, `reports`, `sql`, `src`, `tests`).
- **Environment**: Configured a reproducible Python virtual environment documented in `README.md` and captured in `requirements.txt`.
- **Data Ingestion**: Developed `src/data_ingestion.py` (run via `ingest.py`) to safely load, validate, and normalize the raw UCI dataset without mutating the source file.
- **Data Cleaning**: Developed `src/clean_data.py` (run via `clean.py`) to handle missing values, duplicates, negative quantities, zero prices, and irrelevant non-product transactions based on deliberate analytical decisions.
- **Database Architecture**: Built a deterministic SQLite database (`build_db.py` leveraging `src/build_database.py`) mapped perfectly to pandas outputs, with performance-optimized indices.
- **SQL Exploration**: Authored `sql/01_exploration.sql` containing clean, readable, and business-focused queries. Validated via `run_exploration.py`.
- **Automated Testing**: Created a comprehensive data-quality test suite using `pytest` in `tests/test_data_quality.py`.

## Dataset Statistics
- **Source**: UCI Online Retail Dataset (`Online Retail.xlsx`)
- **Initial Raw Rows**: 541,909
- **Initial Raw Columns**: 8

## Cleaning Statistics
- **Final Row Count**: 348,914 (35.6% reduction primarily due to missing Customer IDs and filtering to the UK cohort)
- **Unique Customers**: 3,917
- **Unique Invoices**: 16,590
- **Total Revenue**: £7,244,495.32
- **Date Range**: 2010-12-01 to 2011-12-09

## Database Statistics
- **Technology**: SQLite (`database/valuelens.db`)
- **Table**: `sales`
- **Indices**: `idx_customerid`, `idx_invoiceno`, `idx_invoicedate`
- **Integrity**: Row counts and revenue exactly match the cleaned pandas DataFrame.

## Test Results
- **Framework**: `pytest`
- **Coverage**: 11 targeted data quality tests validating both the flat CSV outputs and the SQLite tables.
- **Status**: 11/11 tests passing. Zero failures.

## Refactoring & Fixes Applied
During the Phase 1 audit, the following structural improvements were made:
- **Module Structure**: Refactored `src/clean_data.py` and `src/build_database.py` to act purely as importable modules without side effects on import. Extracted their execution logic into top-level runner scripts (`clean.py` and `build_db.py`). This resolves `sys.path` dependency issues, strictly follows Python best practices, and ensures the codebase is highly polished and reproducible for an interview review.

## Remaining Work
- **Phase 2 (RFM Analytics)**: Calculate Recency, Frequency, and Monetary scores per customer via SQL/Pandas.
- **Phase 3 (Segmentation & Modeling)**: Cluster customers (e.g., using K-Means or heuristic quantiles) into actionable business groups.
- **Phase 4 (Insights & Presentation)**: Generate automated visualizations and build the final slide deck summarizing retention strategies.
