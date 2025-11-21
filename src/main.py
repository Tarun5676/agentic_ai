# src/main.py
import os
import pandas as pd
import argparse
from Agents.intake import intake
from Agents.forecasting import forecast
from Agents.matching import match
from Agents.hr_upskilling import hr_upskill
from Agents.analytics import analytics

# ----------------------------------------------------------------------
# 1. HARD-CODED PATHS (edit these two lines)
# ----------------------------------------------------------------------
BENCH_PATH = r"C:\Users\ASUS\Downloads\Bench_Candidates.xlsx"
REQ_PATH   = r"C:\Users\ASUS\Downloads\Project_Requirements.xlsx"

# ----------------------------------------------------------------------
# 2. OPTIONAL: default output location (you can change it later)
# ----------------------------------------------------------------------
DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__), '..', 'agentic_ai_output.xlsx')

# ----------------------------------------------------------------------
def main(bench_path: str, req_path: str, output_path: str = None):
    print("Agentic AI with Grok API – Starting...")
    output_path = output_path or DEFAULT_OUTPUT

    print(f"Loading:\n  Bench: {bench_path}\n  Requirements: {req_path}")

    # 1. Intake (local prep)
    bench_df, req_df, bench_summary, req_summary = intake(bench_path, req_path)

    # 2. Forecasting (Grok)
    print("2. Forecasting with Grok...")
    forecast_df = forecast(req_summary)

    # 3. Matching (Grok)
    print("3. Matching with Grok...")
    _, gap_df = match(forecast_df, bench_summary)

    # 4. HR / Upskilling (Grok)
    print("4. Upskilling & Hiring Recommendations...")
    upskill_df, hire_df = hr_upskill(gap_df, bench_summary, req_summary)

    # 5. Analytics (Grok)
    print("5. Analytics Insights...")
    analytics(forecast_df, gap_df)

    # ---- Save Excel ----------------------------------------------------
    with pd.ExcelWriter(output_path) as writer:
        if not upskill_df.empty:
            upskill_df.to_excel(writer, sheet_name='Upskill Suggestions', index=False)
        if not hire_df.empty:
            hire_df.to_excel(writer, sheet_name='External Hires', index=False)

    print(f"Output saved: {output_path}")

# ----------------------------------------------------------------------
if __name__ == "__main__":
    # ---- CLI mode (still works if you want to override) -------------
    parser = argparse.ArgumentParser(
        description="Agentic AI – Resource Planning with Grok"
    )
    parser.add_argument(
        "--bench", type=str, default=BENCH_PATH,
        help="Path to Bench_Candidates.xlsx (default: hard-coded)"
    )
    parser.add_argument(
        "--req", type=str, default=REQ_PATH,
        help="Path to Project_Requirements.xlsx (default: hard-coded)"
    )
    parser.add_argument(
        "--output", type=str, default=DEFAULT_OUTPUT,
        help="Output Excel path (default: project root)"
    )
    args = parser.parse_args()

    main(args.bench, args.req, args.output)