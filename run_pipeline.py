import subprocess
import os
import sys

def run_step(script_name, step_description):
    """Executes a python script and handles errors."""
    print(f"\n[{step_description}]")
    print(f"Running {script_name}...")
    
    script_path = os.path.join("src", script_name)
    if not os.path.exists(script_path):
        print(f"❌ Error: Could not find script at {script_path}")
        sys.exit(1)
        
    try:
        # Run the script using the current python executable
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Success: {script_name} completed.")
        # Print the script's output to keep logging transparent
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip().split(chr(10))[-1]}") # print just last line to reduce noise
    except subprocess.CalledProcessError as e:
        print(f"❌ FATAL ERROR in {script_name}:")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        print("Pipeline aborted.")
        sys.exit(1)

import time
import sqlite3
import yaml

def execute_sql_layer(conn, layer_name, sql_file, config):
    """Executes a SQL file, measures runtime, and logs row counts."""
    print(f"\n[Executing SQL Layer: {layer_name}]")
    start_time = time.time()
    
    with open(sql_file, 'r') as f:
        sql = f.read()
        
    # Interpolate variables based on config
    if "int_monthly_snapshots" in sql_file:
        ref_date = config['pipeline']['analysis_reference_date']
        if ref_date == 'dynamic':
            ref_date = conn.execute("SELECT date(MAX(invoicedate)) FROM sales").fetchone()[0]
        
        sql = sql.replace('{ANALYSIS_REFERENCE_DATE}', f"'{ref_date}'")
        sql = sql.replace('{LOOKBACK_WINDOW}', str(config['pipeline']['lookback_window_in_months']))
        
    if "mart_customer_rfm_scores_monthly" in sql_file:
        sql = sql.replace('{NUM_QUINTILES}', str(config['rfm']['number_of_quintiles']))
        
    # Create the view
    view_name = os.path.basename(sql_file).replace('.sql', '')
    conn.execute(f"DROP VIEW IF EXISTS {view_name}")
    conn.execute(f"CREATE VIEW {view_name} AS {sql}")
    
    # Query row count
    count = conn.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
    
    runtime = time.time() - start_time
    print(f"✅ Success: Created view {view_name}")
    print(f"   ⏱️ Runtime: {runtime:.2f} seconds")
    print(f"   📊 Row Count: {count:,} rows")

def load_config():
    with open("config.yaml", 'r') as f:
        return yaml.safe_load(f)

def main():
    print("=" * 60)
    print("💎 ValueLens: End-to-End Execution Pipeline")
    print("=" * 60)
    
    # 0. Data Quality Gate
    run_step("data_quality_audit.py", "Stage 0: Data Quality Audit Gate")
    
    # 1. Ingestion
    raw_data_path = os.path.join("data", "raw", "online_retail.csv")
    if os.path.exists(raw_data_path):
        print("Raw dataset found. Skipping ingestion phase to prevent redundant downloading.")
    else:
        run_step("data_ingestion.py", "Stage 1: Data Ingestion")
        
    # 2. Database Build
    run_step("clean_data.py", "Stage 2: Data Cleaning")
    run_step("build_database.py", "Stage 3: SQLite Database Creation")
        
    # 3. SQL Orchestration (Layers)
    config = load_config()
    db_path = os.path.join("database", "valuelens.db")
    print(f"\n[Connecting to SQLite Database: {db_path}]")
    conn = sqlite3.connect(db_path)
    
    sql_dir = "sql"
    sql_layers = [
        ("Staging", os.path.join(sql_dir, "staging", "stg_sales.sql")),
        ("Intermediate - Snapshots", os.path.join(sql_dir, "intermediate", "int_monthly_snapshots.sql")),
        ("Intermediate - RFM", os.path.join(sql_dir, "intermediate", "int_customer_rfm_monthly.sql")),
        ("Marts - Scores", os.path.join(sql_dir, "marts", "mart_customer_rfm_scores_monthly.sql"))
    ]
    
    for layer_name, sql_file in sql_layers:
        execute_sql_layer(conn, layer_name, sql_file, config)
        
    conn.close()
    
    # 4. Python Orchestration (Remaining ML/Analytics)
    pipeline = [
        ("calculate_rfm.py", "Stage 4: CSV Export"),
        ("segment_rfm.py", "Stage 5: Heuristic Segmentation"),
        ("visualize_rfm.py", "Stage 6: Exploratory Visualizations"),
        ("visualize_segments.py", "Stage 7: Segment Visualizations"),
        ("analyze_concentration.py", "Stage 8: Revenue Concentration (Lorenz Curve)"),
        ("clustering.py", "Stage 9: K-Means Preprocessing"),
        ("evaluate_kmeans.py", "Stage 10: K-Means Evaluation (Elbow/Silhouette)"),
        ("run_kmeans.py", "Stage 11: K-Means Model Execution"),
        ("profile_clusters.py", "Stage 12: Cluster Profiling"),
        ("compare_segments.py", "Stage 13: Algorithmic vs Heuristic Comparison"),
        ("statistical_analysis.py", "Stage 14: Non-Parametric Statistical Testing"),
        ("scenario_analysis.py", "Stage 15: Reactivation Scenario Modeling"),
        ("create_customer_360.py", "Stage 16: Final Customer 360 Dataset Assembly"),
        ("generate_dashboard.py", "Stage 17: Executive Dashboard Generation")
    ]
    
    for script, description in pipeline:
        run_step(script, description)
        
    print("\n" + "=" * 60)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("All datasets, SQL databases, ML clusters, and Markdown dashboards have been regenerated.")
    print("Final analytical asset: reports/dashboard/ValueLens_Dashboard.md")

if __name__ == "__main__":
    main()
