# Data Cleaning Decisions for RFM Analysis

This document outlines the findings from our exploratory data analysis and establishes the rules for cleaning the dataset before performing RFM (Recency, Frequency, Monetary) segmentation.

## 1. Missing CustomerID
- **What the issue is**: Transactions that do not have a customer identifier attached.
- **Frequency**: 135,080 records out of 541,909 (24.93%).
- **Should it be removed?**: Yes.
- **Why it's appropriate for RFM**: RFM analysis is inherently customer-centric. Without a `customerid`, we cannot calculate Recency, Frequency, or Monetary value for an individual. Attributing these transactions to a "dummy" customer would severely skew the analysis.
- **Analytical Bias**: Removing these might under-report overall sales revenue. It biases our understanding towards customers who use accounts/logins versus guest checkouts (assuming guest checkouts do not receive a persistent ID).

## 2. Cancelled Invoices
- **What the issue is**: Invoices starting with the letter 'C', representing cancellations or returns.
- **Frequency**: 9,288 records (1.71%).
- **Should it be removed?**: Yes.
- **Why it's appropriate for RFM**: Including cancellations as regular transactions would artificially inflate a customer's Frequency score while negatively impacting their Monetary score. For standard RFM, we typically filter out cancellations to look purely at positive purchase events.
- **Analytical Bias**: If we drop them without subtracting the revenue from the original purchase, we overstate the Monetary value of customers with high return rates. 

## 3. Negative Quantity
- **What the issue is**: Transactions where the item quantity is less than zero. These largely overlap exactly with cancelled invoices.
- **Frequency**: 10,624 records (1.96%).
- **Should it be removed?**: Yes.
- **Why it's appropriate for RFM**: We are analyzing buying behavior. Negative quantities distort the frequency count and the summation of monetary value.
- **Analytical Bias**: Similar to cancellations, ignoring negative quantities overstates the true retained revenue from customers who frequently return items.

## 4. Zero or Negative UnitPrice
- **What the issue is**: Items priced at £0.00 or lower. These are often manual adjustments, bad debt writing, or free items/samples.
- **Frequency**: 2,517 records (0.46%).
- **Should it be removed?**: Yes.
- **Why it's appropriate for RFM**: Zero-priced items do not contribute to Monetary value and skew Frequency (a customer ordering 100 free samples isn't necessarily a high-value frequent buyer). Negative prices (like 'Adjust bad debt') are accounting artifacts, not customer purchases.
- **Analytical Bias**: Removing free samples might slightly obscure our understanding of marketing campaign effectiveness or customer engagement that doesn't yield immediate revenue.

## 5. Duplicate Records
- **What the issue is**: Rows that are exactly identical across all columns.
- **Frequency**: 5,268 records (0.97%).
- **Should it be removed?**: Yes.
- **Why it's appropriate for RFM**: Duplicate rows artificially inflate both the Frequency (if treated as separate orders, though usually grouped by InvoiceNo) and the Monetary value.
- **Analytical Bias**: If duplicates were actually legitimate system logging artifacts (e.g., same item scanned twice in a physical store without updating the quantity), removing them would underestimate revenue. However, in online retail, quantities are usually aggregated per line item.

## 6. Malformed Dates
- **What the issue is**: Dates that could not be parsed into a valid datetime object.
- **Frequency**: 0 records.
- **Should it be removed?**: Yes (if any exist).
- **Why it's appropriate for RFM**: Recency heavily relies on exact dates to calculate days since the last purchase.
- **Analytical Bias**: Negligible, unless malformed dates disproportionately affect a specific time period.

## 7. Missing Descriptions
- **What the issue is**: Rows without a product description.
- **Frequency**: 1,454 records.
- **Should it be removed?**: No, unless CustomerID is also missing.
- **Why it's appropriate for RFM**: RFM cares about *who* bought, *when*, and for *how much*. What they bought (Description) is irrelevant for basic RFM calculation, so we can keep the transaction as long as Quantity and UnitPrice are valid.
- **Analytical Bias**: Retaining them avoids losing valid monetary transactions just because of a product catalog error.

## 8. Unusual Transaction Values (Non-Product StockCodes)
- **What the issue is**: StockCodes like 'POST' (Postage), 'D' (Discount), 'M' (Manual), 'BANK CHARGES', which represent fees, not products.
- **Frequency**: 2,759 records.
- **Should it be removed?**: Yes.
- **Why it's appropriate for RFM**: RFM should ideally reflect product purchasing behavior. Including postage or bank charges inflates the Monetary value with non-merchandise fees. 
- **Analytical Bias**: Removes shipping revenue from the Monetary calculation. This creates a purer "product value" metric but understates the total cash collected from the customer.

## 9. Country Distribution
- **What the issue is**: The dataset spans multiple countries, but it is heavily skewed.
- **Frequency**: The top countries by transaction volume are:
  - **United Kingdom**: 495,478 records
  - **Germany**: 9,495 records
  - **France**: 8,557 records
  - **EIRE**: 8,196 records
  - **Spain**: 2,533 records
  - **Netherlands**: 2,371 records
  - **Belgium**: 2,069 records
  - **Switzerland**: 2,002 records
  - **Portugal**: 1,519 records
  - **Australia**: 1,259 records
- **Should it be removed?**: No, but we should consider filtering the cohort to only 'United Kingdom'.
- **Why it's appropriate for RFM**: Purchasing behavior, shipping costs, and seasonality differ vastly by country. RFM segments are most actionable when the population is homogenous. A UK-only analysis is standard for this dataset since it comprises ~90% of sales.
- **Analytical Bias**: Removing international customers completely ignores a segment of the business that might have unique high-value characteristics or different wholesale dynamics.
