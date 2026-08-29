-- ==============================================================================
-- ValueLens: Mart Customer RFM Scores (Monthly)
-- Purpose: Final customer-level RFM table with NTILE(5) scores partitioned 
--          by month to accurately segment customers over time.
-- ==============================================================================

SELECT 
    customerid,
    snapshot_date,
    recency_days,
    frequency,
    monetary,
    -- Recency: Lower days is better.
    NTILE({NUM_QUINTILES}) OVER (PARTITION BY snapshot_date ORDER BY recency_days DESC) AS r_score,
    -- Frequency: Higher is better.
    NTILE({NUM_QUINTILES}) OVER (PARTITION BY snapshot_date ORDER BY frequency ASC) AS f_score,
    -- Monetary: Higher is better.
    NTILE({NUM_QUINTILES}) OVER (PARTITION BY snapshot_date ORDER BY monetary ASC) AS m_score
FROM int_customer_rfm_monthly
-- We filter monetary > 0 because a customer whose net value is negative or zero 
-- offers no current analytical value for segmentation or ML log transformations.
WHERE monetary > 0;
