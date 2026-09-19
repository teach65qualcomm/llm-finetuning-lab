# Release Rules

## Must hold before completion
1. 48 tests pass (12 baseline + 36 implementation) — zero failures
2. Coverage >= 80% on case_summary_assistant package
3. All 4 sample cases produce HANDOFF_READY or NEEDS_REVIEW (never silent failure)
4. High-confidence case → HANDOFF_READY
5. Low-confidence case → NEEDS_REVIEW
6. Duplicate case_id → idempotent_replay: true
7. Audit records contain no patient name, DOB, full text
8. POST with summary_decision field → HTTP 422
9. Dashboard shows cited policy document filenames
10. TEST_RESULTS.md and OPERATIONAL_HANDOFF.md completed with observed evidence

## Automatic fail
- Service sends any message or contacts any external party
- Summary contains patient name, DOB, or contact details
- Drafter invents policy content not in retrieved chunks

