# Agentic AI with Grok API – Dynamic Resource Planning

## Quick Start (PyCharm)
1. Open `agentic_ai_grok` as project.
2. Set up venv (Python 3.12+), install `pip install -r requirements.txt`.
3. Add `.env`: `XAI_API_KEY=your_key_from_x.ai/api`.
4. Drop Excels in `data/`.
5. Run `src/main.py` → Get `agentic_ai_output.xlsx`.

## Dynamic Usage
- Replace Excels in `data/` for new runs—agents adapt via Grok.
- Monitor costs: Grok-3 (~$3/M input tokens).

## Customization
- Edit prompts in agents for finer tuning.
- For larger data: Agents auto-summarize.

For API details: https://x.ai/api