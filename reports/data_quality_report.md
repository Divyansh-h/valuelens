# Data Quality Audit Report

This report contains the results of the data quality audit on the raw dataset. Both SQL and Python (Pandas) methods were used to verify the integrity of the data.

**Total Rows in Raw Dataset:** 541,909

## 1. Duplicate Transaction Rows
*Rows that have identical values across Invoice, StockCode, Quantity, Date, and Customer.*
*   **Python Check (pandas.duplicated):** 5,268 rows (0.97%)
*   **SQL Check:** 5,429 rows (1.00%)

## 2. Negative Quantities (Refunds/Cancellations)
*Rows where the Quantity is less than zero, indicating a return or cancellation.*
*   **Python Check (Quantity < 0):** 10,624 rows (1.96%)
*   **SQL Check:** 10,624 rows (1.96%)

## 3. Missing Customer IDs
*Transactions that lack a Customer ID, making them impossible to track for RFM analysis.*
*   **Python Check (isnull):** 135,080 rows (24.93%)
*   **SQL Check:** 135,080 rows (24.93%)

## 4. Inconsistent Currency/Units (Zero or Negative Prices)
*Items that have a Unit Price of £0.00 or less, which could represent errors, bad data, or manual adjustments.*
*   **Python Check (UnitPrice <= 0):** 2,517 rows (0.46%)
*   **SQL Check:** 2,517 rows (0.46%)
