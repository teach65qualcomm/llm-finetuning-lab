"""Tests for the FastAPI transport layer — specs/007_api_contract.md."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from case_summary_assistant import repository
from case_summary_assistant.domain import CaseSummary, CitedSection

SAMPLE_CASE = {
    "case_id": "API-TEST-001",
    "payer_id": "PAY001",
    "icd10_code": "I25.10",
    "icd10_prefix": "I",
    "procedure_code": "93306",
    "urgency": "URGENT",
    "age_band": "31-55",
    "diagnosis_category": "Cardiovascular",
    "procedure_type": "Diagnostic imaging",
    "payer_tier": 1,
}


def _fake_draft(case, chunks):
    """Stand-in for the real (LLM-backed) drafter: grounds a citation in the
    real chunk the retriever actually returned, so the reviewer approves it
    without needing a live enterprise AI endpoint."""
    top = chunks[0]
    return CaseSummary(
        patient_context={
            "age_band": case.age_band,
            "diagnosis_category": case.diagnosis_category,
        },
        approved_treatment=case.procedure_type,
        cited_policy_sections=[
            CitedSection(
                source_doc=top.source_doc,
                excerpt=top.chunk_text[:50],
                relevance="Directly grounded in the top retrieved chunk",
            )
        ],
        coverage_notes="Grounded in retrieved policy chunk.",
        recommended_next_steps=["Care manager to review staged summary"],
    )


@pytest.fixture
def client():
    """Reset the real configured database file before each test so api.py's
    endpoints (which use repository's default db_path, not an injectable
    one) run against a clean database, then exercise the app through
    FastAPI's TestClient, which fires the startup event that calls
    repository.init_db()."""
    if repository.DB_PATH.exists():
        repository.DB_PATH.unlink()

    from case_summary_assistant.api import app

    with patch("case_summary_assistant.supervisor.drafter") as md:
        md.draft.side_effect = _fake_draft
        with TestClient(app) as c:
            yield c

    if repository.DB_PATH.exists():
        repository.DB_PATH.unlink()


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "chunk_count" in body


def test_draft_case_returns_200_and_handoff_ready(client):
    resp = client.post("/cases/draft", json=SAMPLE_CASE)
    assert resp.status_code == 200
    body = resp.json()
    assert body["case_id"] == SAMPLE_CASE["case_id"]
    assert body["status"] == "HANDOFF_READY"
    assert body["idempotent_replay"] is False
    assert body["summary"] is not None
    assert body["retrieved_chunks"]


def test_draft_rejects_forbidden_field(client):
    bad_payload = dict(SAMPLE_CASE, case_id="API-TEST-002", summary_decision="APPROVED")
    resp = client.post("/cases/draft", json=bad_payload)
    assert resp.status_code == 422


def test_draft_is_idempotent_on_replay(client):
    first = client.post("/cases/draft", json=SAMPLE_CASE)
    second = client.post("/cases/draft", json=SAMPLE_CASE)
    assert first.status_code == 200 and second.status_code == 200
    assert second.json()["idempotent_replay"] is True
    assert second.json()["case_id"] == first.json()["case_id"]


def test_list_cases_and_get_case(client):
    client.post("/cases/draft", json=SAMPLE_CASE)

    cases = client.get("/cases").json()
    assert any(c["case_id"] == SAMPLE_CASE["case_id"] for c in cases)

    one = client.get(f"/cases/{SAMPLE_CASE['case_id']}")
    assert one.status_code == 200
    assert "audit_events" in one.json()
    assert len(one.json()["audit_events"]) == 4


def test_get_unknown_case_404(client):
    resp = client.get("/cases/DOES-NOT-EXIST")
    assert resp.status_code == 404


def test_audit_log_populated(client):
    client.post("/cases/draft", json=SAMPLE_CASE)
    events = client.get("/audit-log").json()
    agent_names = {e["agent_name"] for e in events}
    assert {"RETRIEVER", "DRAFTER", "REVIEWER", "HANDOFF_ASSEMBLY"} <= agent_names


def test_handoff_queue_lists_case(client):
    client.post("/cases/draft", json=SAMPLE_CASE)
    queue = client.get("/handoff-queue").json()
    assert any(c["case_id"] == SAMPLE_CASE["case_id"] for c in queue)


def test_dashboard_shows_cited_doc(client):
    client.post("/cases/draft", json=SAMPLE_CASE)
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert "BlueCross" in resp.text or "Aetna" in resp.text or ".txt" in resp.text
