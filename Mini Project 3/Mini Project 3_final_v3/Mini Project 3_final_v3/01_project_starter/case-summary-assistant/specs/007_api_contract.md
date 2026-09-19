# 007 — API Contract

## Endpoints
GET  /health           → {status, version, chunk_count}
POST /cases/draft      → HandoffPackage
GET  /cases            → list of case summaries sorted by drafted_at desc
GET  /cases/{case_id}  → one case + agent audit events
GET  /audit-log        → all agent_audit_events (append-only)
GET  /handoff-queue    → HANDOFF_READY and NEEDS_REVIEW cases
GET  /dashboard        → HTML showing queue, confidence scores, cited docs

## Stability requirements
- POST /cases/draft returns 200 (never 201)
- Forbidden fields (summary_decision, send_message, approved) → HTTP 422
- Dashboard shows cited policy document filenames
- /handoff-queue sorted by drafted_at descending
