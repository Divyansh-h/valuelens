import sqlite3
conn = sqlite3.connect(':memory:')
query = """
WITH RECURSIVE month_starts AS (
    SELECT date('2010-12-01') AS dt
    UNION ALL
    SELECT date(dt, '+1 month')
    FROM month_starts
    WHERE dt < '2011-12-01'
),
month_ends AS (
    SELECT date(dt, '+1 month', '-1 day') as snapshot_date 
    FROM month_starts
)
SELECT * FROM month_ends;
"""
for row in conn.execute(query):
    print(row)
