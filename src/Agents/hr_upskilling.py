import json
import pandas as pd
from .forecasting import call_grok

RELATED_SKILLS = {
    "Java": ["Spring Boot"], "Spring Boot": ["Java"],
    "Python": ["Django", "Flask"], "ReactJS": ["Angular", "NodeJS"],
    "Devops": ["AWS Cloud", "Azure Cloud"], "AWS Cloud": ["Devops"],
    "Testing - Manual": ["Testing - Automation"], "Android Development": ["Kotlin"],
    "Business Analysis": ["Project Management"], "Machine Learning": ["Python"]
    # Add more as needed
}

def hr_upskill(gap_df: pd.DataFrame, bench_summary: list, req_summary: list):
    prompt = f"""
    You are an HR/Upskilling Agent. Suggest:
    1. Upskilling existing bench employees (if adjacent skill)
    2. External hires for true gaps

    Gaps: {gap_df.to_json(orient='records')}
    Bench: {json.dumps(bench_summary[:30], indent=2)}
    Requirements: {json.dumps(req_summary[:30], indent=2)}
    Related Skills: {json.dumps(RELATED_SKILLS)}

    Output **only JSON** with two keys:
    {{
      "upskills": [{{"Employee Id": 123, "Suggestion": "Train in X", "Reason": "..."}}],
      "hires": [{{"Project": "A1", "Skills": "X", "Level": "L2", "Count": 1, "Reason": "..."}}]
    }}
    """
    raw = call_grok(prompt)
    try:
        result = json.loads(raw.strip("```json").strip("```"))
        upskills = pd.DataFrame(result.get("upskills", []))
        hires = pd.DataFrame(result.get("hires", []))
        return upskills, hires
    except Exception as e:
        print(f"HR JSON parse error: {e}")
        return pd.DataFrame(), pd.DataFrame()