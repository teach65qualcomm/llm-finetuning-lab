# 005 — Supervisor Contract

## Stage sequence (fixed)
1. RETRIEVAL        — retriever.retrieve(case)
2. DRAFTING         — drafter.draft(case, chunks)
3. REVIEW           — reviewer.review(summary, chunks)
4. HANDOFF_ASSEMBLY — build HandoffPackage

## Early stop
If any sub-agent raises an exception → return HandoffPackage(status=PIPELINE_ERROR)
Do not proceed to later stages.

## Status rules
- review.recommendation == APPROVE → status = HANDOFF_READY
- review.recommendation == FLAG_FOR_HUMAN → status = NEEDS_REVIEW
- any sub-agent exception → status = PIPELINE_ERROR

## HandoffPackage fields
case_id, summary, retrieved_chunks, review_result, confidence_score,
status, error_reason, drafted_at

## Constraints
- Never send a message or contact any external system
- Never expose send/notify functionality even in error handling
- Produce one AgentAuditEvent per executed stage
