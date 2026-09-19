# Prompt 9 — Release Review
Run the full suite and confirm all release conditions are met.

```bash
python -m pytest --cov=case_summary_assistant --cov-report=term-missing --cov-fail-under=80
```

Checklist:
- [ ] 48 tests pass (12 baseline + 36 implementation + your 4 RAG-quality tests)
- [ ] Coverage >= 80%
- [ ] All 4 sample cases produce HANDOFF_READY or NEEDS_REVIEW
- [ ] Duplicate case → idempotent_replay: true
- [ ] Audit records contain no PII or full text
- [ ] POST with summary_decision → 422
- [ ] Dashboard shows cited policy filenames
- [ ] TEST_RESULTS.md and OPERATIONAL_HANDOFF.md completed
