# src/agents/intake.py
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

def parse_month_year(date_str: str) -> datetime:
    current = datetime(2025, 11, 10)
    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4}
    try:
        mon, yr = str(date_str).split()
        month = month_map.get(mon[:3], 1)
        year = 2000 + int(yr[-2:])
        dt = datetime(year, month, 1)
        if dt < current:
            dt += relativedelta(years=1)
        return dt
    except:
        return current

def intake(bench_path: str, req_path: str):
    print("Reading Excel files...")
    bench_df = pd.read_excel(bench_path)
    req_df = pd.read_excel(req_path)

    # --- Normalize Skills into lists ---
    bench_df['Skill_List'] = bench_df['Skill'].apply(
        lambda x: [s.strip() for s in str(x).split(',')] if pd.notna(x) else []
    )
    req_df['Skills_List'] = req_df['Skills'].apply(
        lambda x: [s.strip() for s in str(x).split(',')] if pd.notna(x) else []
    )

    # --- Filter active requirements (forgiving version) ---
    print(f"Total requirements loaded: {len(req_df)}")
    req_df = req_df[
        (req_df['Dropped Reason'] == 'N/A') |
        (req_df['Dropped Reason'].isna()) |
        (req_df['Dropped Reason'] == '') |
        (req_df['Dropped Reason'].astype(str).str.strip() == '')
    ]
    print(f"Active requirements after filter: {len(req_df)}")

    # --- Parse dates ---
    req_df['Requirement Date'] = req_df['Requirement Date'].apply(parse_month_year)

    # --- EXPLODE requirements BEFORE grouping (THIS FIXES THE ERROR) ---
    req_exploded = req_df.explode('Skills_List').copy()
    req_exploded = req_exploded[req_exploded['Skills_List'].notna() & (req_exploded['Skills_List'] != '')]

    # --- Deduplicate and aggregate properly ---
    req_summary = (
        req_exploded.groupby(['Raised', 'Requirement Date', 'Level of Experience', 'Skills_List'])
        .agg({'Resource Count': 'sum'})
        .reset_index()
        .sort_values('Resource Count', ascending=False)
        .head(100)
        .to_dict('records')
    )

    # --- BENCH SUMMARY (also exploded) ---
    bench_exploded = bench_df.explode('Skill_List').copy()
    bench_exploded = bench_exploded[bench_exploded['Skill_List'].notna() & (bench_exploded['Skill_List'] != '')]

    bench_summary = (
        bench_exploded.groupby(['Level of Experience', 'Skill_List'])
        .size()
        .reset_index(name='Available Count')
        .sort_values('Available Count', ascending=False)
        .head(50)
        .to_dict('records')
    )

    # --- PRETTY PRINT TO CONSOLE (NOW 100% SAFE FOR forecasting.py TOO) ---
    print("\n" + "=" * 70)
    print("BENCH SUMMARY (Top 50 skills available)")
    print("=" * 70)
    print(json.dumps(bench_summary, indent=2, ensure_ascii=False))

    print("\n" + "=" * 70)
    print("REQUIREMENTS SUMMARY (Active project needs)")
    print("=" * 70)

    # THIS IS THE FIX: Clean Timestamps BEFORE returning req_summary
    req_summary_clean = []
    for item in req_summary:
        item_copy = item.copy()
        if 'Requirement Date' in item_copy and pd.notnull(item_copy['Requirement Date']):
            # Convert Timestamp → string in the format your forecasting.py expects
            item_copy['Requirement Date'] = item_copy['Requirement Date'].strftime('%b %Y')
        req_summary_clean.append(item_copy)

    # Print the clean version
    print(json.dumps(req_summary_clean, indent=2, ensure_ascii=False))
    print("=" * 70 + "\n")

    # RETURN THE CLEAN VERSION SO forecasting.py NEVER SEES Timestamp
    return bench_df, req_df, bench_summary, req_summary_clean