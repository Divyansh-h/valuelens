# ValueLens Data Lineage

This document outlines the data lineage of the ValueLens pipeline, specifically focusing on the longitudinal RFM snapshot architecture and heuristic segmentation.

## Lineage Diagram

```mermaid
graph TD
    %% Define styles
    classDef raw fill:#f2f2f2,stroke:#b3b3b3,stroke-width:1px,color:#333
    classDef staging fill:#e6f2ff,stroke:#66b3ff,stroke-width:1px,color:#333
    classDef intermediate fill:#fff2e6,stroke:#ffb366,stroke-width:1px,color:#333
    classDef mart fill:#e6ffe6,stroke:#66ff66,stroke-width:1px,color:#333
    classDef output fill:#ffe6e6,stroke:#ff6666,stroke-width:1px,color:#333
    classDef config fill:#ffffcc,stroke:#ffcc00,stroke-width:1px,color:#333

    %% Config
    Config[config.yaml]:::config

    %% Source Data Layer
    RawCSV[Raw CSV Data<br/>data/raw/data.csv]:::raw
    SQLiteRaw[(SQLite Table<br/>sales)]:::raw

    %% Staging Layer
    StgSales[Staging View<br/>stg_sales]:::staging

    %% Intermediate Layer
    IntSnapshots[Intermediate View<br/>int_monthly_snapshots]:::intermediate
    IntRFM[Intermediate View<br/>int_customer_rfm_monthly]:::intermediate

    %% Mart Layer
    MartScores[Mart View<br/>mart_customer_rfm_scores_monthly]:::mart

    %% Processing & Output Layer
    RFM_CSV[Analytical Dataset<br/>data/processed/customer_rfm.csv]:::output
    Segmented_CSV[Segmented Dataset<br/>data/processed/customer_rfm.csv]:::output

    %% Relationships
    RawCSV -- "build_database.py" --> SQLiteRaw
    SQLiteRaw -- "stg_sales.sql<br/>Cleans headers/types" --> StgSales
    
    Config -. "Provides Date Window" .-> IntSnapshots
    StgSales -- "int_monthly_snapshots.sql<br/>Generates date spine" --> IntSnapshots
    
    StgSales -- "int_customer_rfm_monthly.sql<br/>Aggregates RFM metrics per month" --> IntRFM
    IntSnapshots --> IntRFM
    
    Config -. "Provides NTILE count" .-> MartScores
    IntRFM -- "mart_customer_rfm_scores_monthly.sql<br/>Calculates quintiles" --> MartScores
    
    MartScores -- "calculate_rfm.py<br/>Extracts to CSV" --> RFM_CSV
    
    RFM_CSV -- "segment_rfm.py<br/>Applies heuristic rules" --> Segmented_CSV
```

## Description of Layers

1.  **Raw Layer**: Unstructured input data (`data/raw/data.csv`) is ingested and loaded as a raw SQL table in SQLite (`sales`).
2.  **Staging Layer**: The `stg_sales` view performs minimal, fundamental transformations like casting dates and ensuring column names are clean.
3.  **Intermediate Layer**: 
    *   `int_monthly_snapshots` recursively builds the time boundaries for our monthly evaluation windows, dynamically controlled by `config.yaml`.
    *   `int_customer_rfm_monthly` aggregates lifetime metrics (Recency, Frequency, Monetary) for each customer *as of* every month-end snapshot date.
4.  **Mart Layer**: `mart_customer_rfm_scores_monthly` applies `NTILE()` window functions to rank customers into quintiles (1-5 scale) against their peers at that specific point in time, producing RFM scores.
5.  **Output & Segmentation Layer**: The SQL results are extracted into a CSV format (`data/processed/customer_rfm.csv`). The `segment_rfm.py` Python script then applies business rules to assign human-readable segments (e.g., "Champions", "Lost") based on the RFM scores.
