# ValueLens — Customer Value Segmentation & Retention Analytics

## Business Problem
In many businesses, customer retention and maximizing customer lifetime value (CLV) are critical to long-term profitability. However, companies often struggle to differentiate between high-value, at-risk, and churned customers, leading to inefficient marketing spend and generic retention strategies. The challenge is to identify customer segments based on their behavior and value, and to deploy targeted strategies to increase retention and overall profitability.

## Project Objective
**ValueLens** aims to analyze customer transaction data to segment the customer base using RFM (Recency, Frequency, Monetary) analysis and predictive modeling. The primary objectives are to:
1. Clean and transform raw transaction data into a robust analytical dataset.
2. Segment customers based on their purchasing behavior.
3. Identify at-risk customers and predict potential churn.
4. Provide actionable, data-driven recommendations to improve customer retention and maximize lifetime value.
5. Present the findings through professional visualizations and a structured presentation suitable for a business audience.

## Methodology
The project will follow a structured data science workflow:
1. **Data Ingestion & Cleaning**: Processing raw transaction data, handling missing values, anomalies, and ensuring data quality using Python and SQL.
2. **Exploratory Data Analysis (EDA)**: Uncovering patterns, trends, and initial insights using pandas, matplotlib, and seaborn.
3. **Customer Segmentation**: Implementing RFM analysis and clustering techniques (e.g., K-Means via scikit-learn) to group customers based on their value.
4. **Predictive Analytics**: Developing models to predict customer churn or future value.
5. **Business Insights Generation**: Translating analytical results into strategic business recommendations.
6. **Reporting**: Creating clear, automated reports and a presentation to communicate findings to stakeholders.

## Technology Stack
- **Languages**: Python, SQL
- **Database**: SQLite (for localized data querying and manipulation)
- **Data Manipulation**: pandas, NumPy
- **Machine Learning**: scikit-learn
- **Data Visualization**: matplotlib, seaborn
- **Reporting/Exporting**: openpyxl (Excel), python-pptx (PowerPoint)
- **Development Environment**: Jupyter Notebooks

## Environment Setup
To run this project, it is recommended to use a virtual environment. Follow these steps to set up the environment and install dependencies:

1. Clone the repository and navigate to the project directory:
   ```bash
   cd ValueLens
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   - On macOS/Linux: `source .venv/bin/activate`
   - On Windows: `.venv\Scripts\activate`

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Data Ingestion
To load and validate the raw dataset into the project, you can run the ingestion pipeline. This script verifies the dataset schema, normalizes column names, and checks that critical information like `invoicedate` can be properly parsed before any business logic or cleaning is applied.

Run the pipeline from the project root:
```bash
python3 ingest.py
```

## Expected Outputs
- A clean, reproducible data pipeline.
- SQLite database containing processed analytical tables.
- Jupyter notebooks detailing the EDA, segmentation, and modeling steps.
- Python scripts modularizing the core logic (`src/`).
- Exported data reports (Excel) highlighting key customer segments.
- A final presentation slide deck outlining the business problem, methodology, insights, and strategic recommendations.

## Project Structure
```text
ValueLens/
├── data/
│   ├── raw/             # Raw, immutable data
│   ├── processed/       # Cleaned and transformed data ready for analysis
│   └── exports/         # Data exports for reporting (e.g., Excel files)
├── database/            # SQLite database files
├── notebooks/           # Jupyter notebooks for exploration and analysis
├── src/                 # Python source code for data processing and modeling
├── sql/                 # SQL scripts for data extraction and transformation
├── tests/               # Unit tests for source code
├── reports/             # Generated analysis reports
├── presentation/        # Presentation materials (e.g., PPTX)
├── requirements.txt     # Python dependencies
├── README.md            # Project overview and instructions
└── .gitignore           # Git ignored files and directories
```
