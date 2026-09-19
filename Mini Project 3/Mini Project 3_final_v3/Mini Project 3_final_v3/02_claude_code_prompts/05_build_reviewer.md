# Prompt 5 — Build the Review Agent (Task 3)
Implement review() in reviewer.py. Pure Python — no LLM calls.

Steps:
1. Lowercase all chunk text for matching
2. For each cited_policy_section, check if excerpt appears in chunk text
3. confidence_score = verified / total (1.0 if no citations)
4. FLAG_FOR_HUMAN if confidence_score < CONFIDENCE_THRESHOLD (0.70)
5. Return ReviewResult

Run: `python -m pytest tests/test_reviewer.py -q`
All tests must pass including below-threshold and empty-citation cases.
