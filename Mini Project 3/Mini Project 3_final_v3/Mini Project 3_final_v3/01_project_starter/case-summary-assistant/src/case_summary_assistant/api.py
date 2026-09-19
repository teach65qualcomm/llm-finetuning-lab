"""FastAPI transport layer."""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Optional
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from case_summary_assistant import repository, service
from case_summary_assistant.domain import PriorAuthCase

app = FastAPI(title="Case-Summary Drafting Assistant", version="1.0.0")


class DraftRequest(BaseModel):
    case_id: str
    payer_id: str
    icd10_code: str
    icd10_prefix: str
    procedure_code: str
    urgency: str
    age_band: str
    diagnosis_category: str
    procedure_type: str
    payer_tier: int

    model_config = {"extra": "forbid"}   # 422 on forbidden fields


@app.on_event("startup")
def startup():
    repository.init_db()


@app.get("/health")
def health():
    try:
        import chromadb
        from case_summary_assistant.llm_config import CHROMA_PATH, CHROMA_COLLECTION
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        col = client.get_collection(CHROMA_COLLECTION)
        chunk_count = col.count()
    except Exception:
        chunk_count = 0
    return {"status": "ok", "version": "1.0.0", "chunk_count": chunk_count}


@app.post("/cases/draft")
def draft_case(req: DraftRequest):
    case = PriorAuthCase(**req.model_dump())
    result = service.evaluate(case)
    return {
        "case_id": result.case_id,
        "status": result.status,
        "confidence_score": result.confidence_score,
        "error_reason": result.error_reason,
        "drafted_at": result.drafted_at.isoformat(),
        "idempotent_replay": result.idempotent_replay,
        "summary": vars(result.summary) if result.summary else None,
        "retrieved_chunks": [vars(c) for c in result.retrieved_chunks],
        "review_result": vars(result.review_result) if result.review_result else None,
    }


@app.get("/cases")
def list_cases():
    return repository.list_cases()


@app.get("/cases/{case_id}")
def get_case(case_id: str):
    row = repository.find_by_case_id(case_id)
    if not row:
        raise HTTPException(status_code=404, detail="Case not found")
    row["audit_events"] = repository.get_audit_events(case_id)
    return row


@app.get("/audit-log")
def audit_log():
    conn = repository.get_connection()
    rows = conn.execute("SELECT * FROM agent_audit_events ORDER BY executed_at").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/handoff-queue")
def handoff_queue():
    return repository.list_handoff_queue()


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    cases = repository.list_handoff_queue()
    rows = ""
    for c in cases:
        status = c.get("status", "—")
        color = {"HANDOFF_READY": "#d4edda", "NEEDS_REVIEW": "#fff3cd"}.get(status, "#f8d7da")
        score = f"{c.get('confidence_score', 0):.2f}" if c.get("confidence_score") else "—"
        docs = c.get("retrieved_doc_sources", "—")
        rows += f'<tr style="background:{color}"><td>{status}</td><td>{c["case_id"]}</td><td>{score}</td><td style="font-size:11px">{docs}</td><td>{c["drafted_at"][:19]}</td></tr>'
    return f"""
    <html><head><title>Handoff Queue</title></head><body>
    <h2>Case-Summary Handoff Queue</h2>
    <table border="1" cellpadding="6">
    <tr><th>Status</th><th>Case ID</th><th>Confidence</th><th>Cited Docs</th><th>Drafted At</th></tr>
    {rows or '<tr><td colspan=5>No cases yet. POST to /cases/draft first.</td></tr>'}
    </table></body></html>
    """
