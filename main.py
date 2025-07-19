import subprocess
import sys

def run_script(script):
    print(f"\n=== Running {script} ===")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Error running {script}. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    scripts = [
        'djia_data_fetch.py',
        'djia_daily_returns.py',
        'djia_lowest_returns.py',
        'djia_trading_simulation.py',
        'djia_performance_metrics.py',
        'dia_comparison.py',
        'side_by_side_metrics.py',
        'plotly_visualization.py',
    ]
    for script in scripts:
        run_script(script)
    print("\nAll steps completed successfully!") 