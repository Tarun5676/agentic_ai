import json
import pandas as pd
from .forecasting import call_grok

def match(forecast_df: pd.DataFrame, bench_summary: list):
    prompt = f"""
    You are a Matching Agent. Match forecasted skill demand to available bench employees.
    Forecast: {forecast_df.to_json(orient='records')}
    Bench Summary (skill + count): {json.dumps(bench_summary, indent=2)}

    Output **only JSON** of **unfilled gaps**:
    [
      {{"Skills": "AWS Cloud", "Level of Experience": "L2", "Count": 2}}
    ]
    """
    raw = call_grok(prompt)
    try:
        gaps = json.loads(raw.strip("```json").strip("```"))
        return [], pd.DataFrame(gaps)
    except:
        return [], pd.DataFrame()