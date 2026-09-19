# Case-Summary Drafting Assistant — Mini Project 3
## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/ingest_policies.py
python -m pytest -m baseline -q   # expected: 12 passed, 36 deselected
uvicorn case_summary_assistant.api:app --app-dir src --reload
```
Note: If pytest cannot find the module: `export PYTHONPATH=src`
