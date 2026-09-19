# CLAUDE.md — Case-Summary Drafting Assistant

## Project mission
Build a multi-agent service that retrieves relevant insurance policy document sections (RAG),
drafts a structured case summary, quality-checks it, and stages a handoff package for the
care manager. The service never sends anything, makes a coverage decision, or contacts any
external party on its own.

## Non-negotiable constraints
1. The service must NEVER send a message, email, or notification to any party.
2. HANDOFF_READY means the package is staged — the care manager acts on it.
3. The drafting agent must NEVER invent policy content not in the retrieved chunks.
4. Patient context must exclude name, date of birth, phone, email, and address.
5. Audit records must never contain full summary text, patient PII, or raw chunk content.
6. Do not edit test files unless a test genuinely conflicts with an approved specification.

## Source order (read before modifying)
1. specs/ — implementation authority
2. .claude/rules/ — persistent constraints
3. src/case_summary_assistant/ — code to complete
4. tests/ — proof of correctness

## Key commands
```bash
python scripts/ingest_policies.py                              # ingest policy docs (once)
python -m pytest -m baseline -q                               # 12 baseline tests
python -m pytest tests/test_retriever.py -q                   # Task 1
python -m pytest tests/test_drafter.py -q                     # Task 2
python -m pytest tests/test_reviewer.py -q                    # Task 3
python -m pytest tests/test_supervisor.py -q                  # Task 4
python -m pytest tests/test_repository_service.py -q          # Task 5
python -m pytest --cov=case_summary_assistant --cov-report=term-missing  # full suite
uvicorn case_summary_assistant.api:app --app-dir src --reload  # run service
```
