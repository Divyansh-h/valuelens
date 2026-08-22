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
        print(e.stderr)
        print("Pipeline aborted.")
        sys.exit(1)

def main():
    print("=" * 60)
    print("💎 ValueLens: End-to-End Execution Pipeline")
    print("=" * 60)
    
    # Check if raw data already exists to prevent re-downloading
    raw_data_path = os.path.join("data", "raw", "online_retail.csv")
    if os.path.exists(raw_data_path):
        print("Raw dataset found. Skipping ingestion phase to prevent redundant downloading.")
    else:
        run_step("data_ingestion.py", "Stage 1: Data Ingestion")
        
    # The Ordered Pipeline
    pipeline = [
        ("clean_data.py", "Stage 2: Data Cleaning"),
        ("build_database.py", "Stage 3: SQLite Database Creation"),
        ("calculate_rfm.py", "Stage 4: RFM Calculation"),
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
