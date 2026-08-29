-- ==============================================================================
-- ValueLens: Monthly Snapshots
-- Purpose: Generate a time-series spine of month-end dates based on configuration.
-- ==============================================================================

WITH RECURSIVE month_starts AS (
    -- Start from N months prior to the reference date
    SELECT date({ANALYSIS_REFERENCE_DATE}, 'start of month', '-{LOOKBACK_WINDOW} months') AS dt
    UNION ALL
    -- Increment by exactly 1 month
    SELECT date(dt, '+1 month')
    FROM month_starts
    WHERE dt < date({ANALYSIS_REFERENCE_DATE}, 'start of month')
),
month_ends AS (
    -- Shift to the last day of each month
    SELECT date(dt, '+1 month', '-1 day') as snapshot_date 
    FROM month_starts
)
SELECT snapshot_date 
FROM month_ends;
