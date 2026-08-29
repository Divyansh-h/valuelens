-- ==============================================================================
-- ValueLens: Longitudinal Monthly Customer RFM
-- Purpose: Calculates rolling Recency, Frequency, and Monetary scores for every 
--          customer at the end of every month since their first purchase.
-- ==============================================================================

WITH customers AS (
    -- Identify every customer's acquisition date
    SELECT 
        customerid, 
        date(MIN(invoicedate)) as first_purchase_date
    FROM stg_sales
    GROUP BY customerid
),
customer_snapshots AS (
    -- Cross-join customers against all month-end dates *after* their acquisition
    SELECT 
        c.customerid, 
        m.snapshot_date
    FROM customers c
    CROSS JOIN int_monthly_snapshots m
    WHERE m.snapshot_date >= c.first_purchase_date
)
SELECT
    cs.customerid,
    cs.snapshot_date,
    -- Recency: Days since last positive purchase prior to snapshot date
    CAST(JULIANDAY(cs.snapshot_date) - JULIANDAY(MAX(CASE WHEN s.quantity > 0 THEN s.invoicedate END)) AS INTEGER) AS recency_days,
    -- Frequency: Count of positive purchase invoices up to snapshot date
    COUNT(DISTINCT CASE WHEN s.quantity > 0 THEN s.invoiceno END) AS frequency,
    -- Monetary: Net sum of all purchases and returns up to snapshot date
    ROUND(SUM(s.totalamount), 2) AS monetary
FROM customer_snapshots cs
LEFT JOIN stg_sales s 
    ON s.customerid = cs.customerid 
    -- Only aggregate transactions that occurred ON or BEFORE the snapshot date
    AND date(s.invoicedate) <= cs.snapshot_date
GROUP BY 
    cs.customerid, 
    cs.snapshot_date;
