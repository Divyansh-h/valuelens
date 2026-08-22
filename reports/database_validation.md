# Database Validation Report

The `valuelens.db` SQLite database has been successfully built and populated with the cleaned transaction data.

## Verification Metrics (Queried directly from SQLite)
- **Row Count**: `348,914` (Expected: 348,914)
- **Unique Customers**: `3,917` (Expected: 3,917)
- **Unique Invoices**: `16,590` (Expected: 16,590)
- **Date Range Start**: `2010-12-01 08:26:00` 
- **Date Range End**: `2011-12-09 12:49:00` 
- **Total Revenue**: `£7,244,495.32` (Expected: £7,244,495.32)

## Schema & Indexes
- Table: `sales`
- Indexes Created:
  - `idx_customerid`: Accelerates `GROUP BY customerid` for customer-level RFM aggregations.
  - `idx_invoiceno`: Accelerates invoice-level lookups and basket analyses.
  - `idx_invoicedate`: Accelerates time-series filtering and Recency calculations.
