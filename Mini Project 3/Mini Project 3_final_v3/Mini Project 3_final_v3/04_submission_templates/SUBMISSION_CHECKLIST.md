# Submission Checklist — Mini Project 3

## Tests
- [ ] 48 tests pass (12 baseline + 36 implementation), plus your 4 RAG-quality tests in test_rag_quality.py
- [ ] Coverage >= 80%

## Agent behavior
- [ ] High-confidence case → HANDOFF_READY
- [ ] Low-confidence case → NEEDS_REVIEW with flagged gaps
- [ ] Retrieval failure → PIPELINE_ERROR
- [ ] Duplicate case_id → idempotent_replay: true

## Safety
- [ ] Service does NOT send any message
- [ ] Summary excludes patient name, DOB, phone, email
- [ ] Audit records contain no PII or full text
- [ ] POST with summary_decision → HTTP 422
- [ ] Drafter uses only retrieved chunks (no invented content)
- [ ] Audit UPDATE/DELETE raises error

## Submission files
- [ ] Complete src/case_summary_assistant/ with all tasks implemented
- [ ] data/sample_prior_auth_cases.json present
- [ ] TEST_RESULTS.md completed with observed results
- [ ] OPERATIONAL_HANDOFF.md completed

## Not included
- [ ] .venv/ removed
- [ ] vector_store/ removed (too large; note ingestion instructions)
- [ ] data/*.db removed
- [ ] No real patient data or real policy documents
- [ ] No API keys or credentials
