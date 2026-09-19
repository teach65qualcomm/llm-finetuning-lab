# Prompt 6 — Build the Supervisor (Task 4)
Implement run_pipeline() in supervisor.py.

Stage order: RETRIEVAL → DRAFTING → REVIEW → HANDOFF_ASSEMBLY
Return tuple: (HandoffPackage, list[dict of agent events])
- Any sub-agent exception → PIPELINE_ERROR, return immediately with 1 event
- APPROVE → HANDOFF_READY
- FLAG_FOR_HUMAN → NEEDS_REVIEW
- 4 agent events on full success, 1 on retrieval failure

Run: `python -m pytest tests/test_supervisor.py -q`
Never send a message or call any external system from supervisor.py.
