import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"


def call_grok(prompt: str, model: str = "x-ai/grok-4.1-fast:free"):  # FIXED: Use grok-beta
    if not OPENROUTER_API_KEY:
        print("⚠️ No OPENROUTER_API_KEY – using local fallback")
        return ""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Agentic AI",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 1500
    }

    try:
        print(f"🔄 Calling OpenRouter: {model} | Prompt length: {len(prompt)}")  # Debug
        response = requests.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers, timeout=60)

        if response.status_code == 400:
            print(f"❌ 400 Details: {response.json().get('error', {}).get('message', 'Unknown')}")
            return ""

        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        print(f"✅ Grok ({model}) success: {len(content)} chars")  # Debug
        return content
    except Exception as e:
        print(f"❌ OpenRouter Error: {e}")
        if 'response' in locals():
            print(f"Response body: {response.text[:300]}")
        return ""
def forecast(req_summary: list):
    prompt = f"""
    Analyze this requirements data and forecast skill demand (skill, level, count) for next 90 days.
    Data: {json.dumps(req_summary[:10], indent=2)}  # Limited for tokens

    Output ONLY valid JSON array:
    [{{"Skills": "Spring Boot", "Level of Experience": "L2", "Forecast Count": 3, "Confidence": 0.8}}, ...]
    """
    raw = call_grok(prompt)
    if raw:
        try:
            data = json.loads(raw.strip("```json\n").strip("```"))
            return pd.DataFrame(data)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON from Grok – using fallback.")

    # === FALLBACK: Simple local forecast ===
    print("🔄 Using local forecasting (no API).")
    from collections import Counter
    all_skills = [item['Skills_List'] for item in req_summary if 'Skills_List' in item]
    skill_counts = Counter(all_skills)
    print(all_skills)
    print(skill_counts)

    fallback = []
    for skill, count in skill_counts.most_common(10):
        fallback.append({
            'Skills': skill,
            'Level of Experience': 'L2',  # Default
            'Forecast Count': count,
            'Confidence': 0.7
        })
    return pd.DataFrame(fallback)