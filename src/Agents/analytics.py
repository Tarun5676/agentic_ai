from .forecasting import call_grok

def analytics(forecast_df, gap_df):
    prompt = f"""
    Analytics Summary:
    - Forecasted roles: {len(forecast_df)}
    - Unfilled gaps: {len(gap_df)}

    Give 3 bullet points of insights (e.g., skill shortages, trends).
    """
    print("\nAnalytics Insights:")
    print(call_grok(prompt))