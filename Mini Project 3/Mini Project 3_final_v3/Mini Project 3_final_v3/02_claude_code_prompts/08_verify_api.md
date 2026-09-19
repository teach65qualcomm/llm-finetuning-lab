# Prompt 8 — Verify API and Dashboard
The API is scaffolded. Verify correctness, make only justified fixes.

1. Run: `python -m pytest tests/test_api.py -q` (if it exists)
2. Start: `uvicorn case_summary_assistant.api:app --app-dir src --reload`
3. Test all 4 sample cases from data/sample_prior_auth_cases.json
4. Verify POST with summary_decision field returns 422
5. Open /dashboard — confirm cited policy filenames are visible
6. Submit same case twice — confirm idempotent_replay: true
