# 006 — Persistence and Audit

## handoff_cases table
case_id (PK), payer_id, status, summary_json, confidence_score,
retrieved_doc_sources, error_reason, drafted_at

## agent_audit_events table
event_id (PK), case_id (FK), agent_name, input_hash, output_summary, executed_at

## Transaction requirement
Case insertion and all audit event insertions must succeed or fail together.

## Idempotency
Check case_id before running pipeline. If exists → return stored package with idempotent_replay: true.

## Immutability
agent_audit_events is append-only. Triggers reject UPDATE and DELETE.

## Safe evidence
ALLOWED: confidence_score, status, agent_name, retrieved_doc_sources (filenames only), input_hash
FORBIDDEN: full summary text, full chunk text, patient name, DOB, phone, email
