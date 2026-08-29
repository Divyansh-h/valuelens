-- ==============================================================================
-- ValueLens: Staging Sales
-- Purpose: Extract raw sales data and perform basic cleaning/standardization.
-- ==============================================================================
SELECT 
    invoiceno,
    stockcode,
    description,
    quantity,
    invoicedate,
    unitprice,
    customerid,
    country,
    totalamount
FROM sales;
