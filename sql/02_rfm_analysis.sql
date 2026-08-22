-- ==============================================================================
-- ValueLens: RFM Calculation
-- Purpose: Calculate Recency, Frequency, and Monetary value for each customer,
--          along with their corresponding NTILE(5) scores.
-- ==============================================================================

WITH snapshot AS (
    -- 1. Determine the snapshot date (Max date + 1 day)
    SELECT DATETIME(MAX(invoicedate), '+1 day') AS snapshot_date
    FROM sales
),
customer_rfm AS (
    -- 2-4. Aggregate Recency, Frequency, and Monetary at the customer level
    SELECT 
        s.customerid,
        CAST(JULIANDAY((SELECT snapshot_date FROM snapshot)) - JULIANDAY(MAX(s.invoicedate)) AS INTEGER) AS recency_days,
        COUNT(DISTINCT s.invoiceno) AS frequency,
        ROUND(SUM(s.totalamount), 2) AS monetary
    FROM sales s
    GROUP BY s.customerid
)
-- 5. Calculate R, F, and M scores using NTILE(5)
-- Recency: Lower days is better. ORDER BY recency_days DESC assigns bucket 5 to the smallest days.
-- Frequency: Higher is better. ORDER BY frequency ASC assigns bucket 5 to the highest frequency.
-- Monetary: Higher is better. ORDER BY monetary ASC assigns bucket 5 to the highest monetary value.
SELECT 
    customerid,
    recency_days,
    frequency,
    monetary,
    NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
    NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
    NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
FROM customer_rfm;
