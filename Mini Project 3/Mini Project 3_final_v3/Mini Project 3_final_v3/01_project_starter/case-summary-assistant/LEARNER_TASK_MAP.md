# Learner Task Map

| Task | File | Specification | Proof |
|------|------|---------------|-------|
| 1 — RAG retrieval agent | src/case_summary_assistant/retriever.py | specs/002_retrieval_contract.md | tests/test_retriever.py |
| 2 — Drafting agent | src/case_summary_assistant/drafter.py | specs/003_drafting_contract.md | tests/test_drafter.py |
| 3 — Review agent | src/case_summary_assistant/reviewer.py | specs/004_review_contract.md | tests/test_reviewer.py |
| 4 — Supervisor | src/case_summary_assistant/supervisor.py | specs/005_supervisor_contract.md | tests/test_supervisor.py |
| 5 — Persistence & audit | src/case_summary_assistant/repository.py | specs/006_persistence_and_audit.md | tests/test_repository_service.py |
| 6 — LLM config | src/case_summary_assistant/llm_config.py | specs/003_drafting_contract.md | tests/test_drafter.py |

## Incomplete locations
Each file raises NotImplementedError("Mini Project Task N: <description>") at the gap.
Work in task order. Run focused tests after each task.
