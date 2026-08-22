-- ==============================================================================
-- ValueLens: Business Segment Summary Analytics
-- Purpose: Reproduce the pandas aggregation of business segments using SQL.
--          Relies on the 'customer_rfm' table which contains the Segment column.
-- ==============================================================================

WITH totals AS (
    SELECT 
        COUNT(*) AS grand_total_customers,
        SUM(Monetary) AS grand_total_revenue
    FROM customer_rfm
)
SELECT 
    s.Segment,
    COUNT(s.CustomerID) AS num_customers,
    ROUND(CAST(COUNT(s.CustomerID) AS FLOAT) / t.grand_total_customers * 100, 2) AS pct_customers,
    ROUND(SUM(s.Monetary), 2) AS total_revenue,
    ROUND(SUM(s.Monetary) / t.grand_total_revenue * 100, 2) AS pct_revenue,
    ROUND(AVG(s.Monetary), 2) AS avg_revenue,
    ROUND(AVG(s.Frequency), 2) AS avg_frequency,
    ROUND(AVG(s.Recency), 2) AS avg_recency
    
    -- Note: SQLite does not have a built-in MEDIAN function, so median is calculated via pandas.
FROM customer_rfm s
CROSS JOIN totals t
GROUP BY s.Segment, t.grand_total_customers, t.grand_total_revenue
ORDER BY total_revenue DESC;
