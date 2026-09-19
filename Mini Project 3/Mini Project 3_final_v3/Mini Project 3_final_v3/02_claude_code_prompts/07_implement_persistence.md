# Prompt 7 — Implement Persistence and Audit (Task 5)
Implement save_package() in repository.py.

Rules:
- ONE transaction: handoff_case row + all audit event rows
- summary_json: include only anonymized fields (no patient name, DOB, phone, email)
- output_summary in audit events: short descriptive string only (not full text)
- Do NOT modify the append-only triggers

Run: `python -m pytest tests/test_repository_service.py -q`
All must pass including idempotency, trigger, and PII safety tests.
