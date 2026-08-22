# Data Profile: Online Retail.xlsx

## 1. File Information
- **Filename**: `Online Retail.xlsx`
- **File Size**: `22.62 MB`

## 2. Basic Dimensions
- **Number of Rows**: `541,909`
- **Number of Columns**: `8`
- **Columns**: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

## 3. Data Types
```text
InvoiceNo              object
StockCode              object
Description            object
Quantity                int64
InvoiceDate    datetime64[ns]
UnitPrice             float64
CustomerID            float64
Country                object
```

## 4. Missing Values
```text
InvoiceNo           0
StockCode           0
Description      1454
Quantity            0
InvoiceDate         0
UnitPrice           0
CustomerID     135080
Country             0
```

## 5. Data Quality Issues Identified
- **Duplicate Rows**: `5,268`
- **Negative Quantities**: `10,624` (Likely returns or cancellations)
- **Zero or Negative Unit Prices**: `2,517` (Possible free items, bad data, or debt adjustments)
- **Invoice Cancellations**: `9,288` (Invoices starting with 'C')

## Summary
The dataset contains over half a million rows but exhibits several data quality issues typical of raw transaction logs, including missing `CustomerID` values, negative quantities, zero/negative prices, and duplicates. These will need to be addressed before performing RFM analysis.
