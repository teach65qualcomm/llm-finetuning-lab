"""Tests for persistence and audit — Task 5."""
import pytest, sqlite3
from unittest.mock import patch
from case_summary_assistant.domain import HandoffPackage, ReviewResult, RetrievalError
from datetime import datetime

def make_handoff_package(case_id="TEST-001", status="HANDOFF_READY"):
    from case_summary_assistant.domain import CaseSummary, CitedSection, RetrievedChunk
    summary = CaseSummary(
        patient_context={"age_band": "31-55"}, approved_treatment="Echocardiography",
        cited_policy_sections=[CitedSection(source_doc="BlueCross.txt", excerpt="covered at 90%", relevance="confirms")],
        coverage_notes="90% covered", recommended_next_steps=["Schedule appointment"],
    )
    chunks = [RetrievedChunk(chunk_text="echocardiography covered", source_doc="BlueCross.txt", page_number=2, similarity_score=0.90)]
    review = ReviewResult(confidence_score=0.90, flagged_gaps=[], recommendation="APPROVE")
    return HandoffPackage(
        case_id=case_id, summary=summary, retrieved_chunks=chunks,
        review_result=review, confidence_score=0.90, status=status,
        error_reason=None, drafted_at=datetime.utcnow(),
    )

def make_events():
    return [
        {"agent_name": "RETRIEVER", "input_hash": "abc123", "output_summary": "3 chunks retrieved"},
        {"agent_name": "DRAFTER", "input_hash": "def456", "output_summary": "1 cited section"},
        {"agent_name": "REVIEWER", "input_hash": "ghi789", "output_summary": "confidence=0.90"},
        {"agent_name": "HANDOFF_ASSEMBLY", "input_hash": "jkl012", "output_summary": "HANDOFF_READY"},
    ]

@pytest.mark.baseline
def test_repository_importable():
    from case_summary_assistant import repository
    assert hasattr(repository, "save_package")

@pytest.mark.baseline
def test_init_db_creates_tables(tmp_db):
    conn = sqlite3.connect(str(tmp_db))
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    assert "handoff_cases" in tables
    assert "agent_audit_events" in tables
    conn.close()

@pytest.mark.baseline
def test_audit_triggers_exist(tmp_db):
    conn = sqlite3.connect(str(tmp_db))
    triggers = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='trigger'")]
    assert "no_update_agent_audit" in triggers
    assert "no_delete_agent_audit" in triggers
    conn.close()

@pytest.mark.implementation
def test_save_and_find(tmp_db):
    from case_summary_assistant.repository import save_package, find_by_case_id
    pkg = make_handoff_package()
    save_package(pkg, make_events(), db_path=tmp_db)
    row = find_by_case_id("TEST-001", db_path=tmp_db)
    assert row is not None
    assert row["case_id"] == "TEST-001"
    assert row["status"] == "HANDOFF_READY"

@pytest.mark.implementation
def test_four_audit_events_saved(tmp_db):
    from case_summary_assistant.repository import save_package, get_audit_events
    pkg = make_handoff_package()
    save_package(pkg, make_events(), db_path=tmp_db)
    events = get_audit_events("TEST-001", db_path=tmp_db)
    assert len(events) == 4

@pytest.mark.implementation
def test_idempotency(tmp_db):
    from case_summary_assistant import service
    from case_summary_assistant.domain import ReviewResult
    case = pytest.importorskip("case_summary_assistant.domain").PriorAuthCase(
        case_id="IDEM-001", payer_id="PAY001", icd10_code="I10", icd10_prefix="I",
        procedure_code="93306", urgency="URGENT", age_band="31-55",
        diagnosis_category="Cardiovascular", procedure_type="Diagnostic", payer_tier=1,
    )
    pkg1 = make_handoff_package("IDEM-001")
    events = make_events()
    with patch("case_summary_assistant.service.supervisor") as ms:
        ms.run_pipeline.return_value = (pkg1, events)
        r1 = service.evaluate(case, db_path=tmp_db)
        r2 = service.evaluate(case, db_path=tmp_db)
    assert r2.idempotent_replay is True
    assert r2.case_id == r1.case_id

@pytest.mark.implementation
def test_no_duplicate_on_replay(tmp_db):
    from case_summary_assistant.repository import save_package, list_cases
    pkg = make_handoff_package("DUP-001")
    save_package(pkg, make_events(), db_path=tmp_db)
    cases = list_cases(db_path=tmp_db)
    assert len(cases) == 1

@pytest.mark.implementation
def test_audit_update_forbidden(tmp_db):
    from case_summary_assistant.repository import save_package
    pkg = make_handoff_package("TRIG-001")
    save_package(pkg, make_events(), db_path=tmp_db)
    conn = sqlite3.connect(str(tmp_db))
    with pytest.raises(Exception):
        conn.execute("UPDATE agent_audit_events SET output_summary='tampered'")
        conn.commit()
    conn.close()

@pytest.mark.implementation
def test_audit_delete_forbidden(tmp_db):
    from case_summary_assistant.repository import save_package
    pkg = make_handoff_package("TRIG-002")
    save_package(pkg, make_events(), db_path=tmp_db)
    conn = sqlite3.connect(str(tmp_db))
    with pytest.raises(Exception):
        conn.execute("DELETE FROM agent_audit_events")
        conn.commit()
    conn.close()

@pytest.mark.implementation
def test_audit_no_full_text(tmp_db):
    from case_summary_assistant.repository import save_package
    pkg = make_handoff_package("PII-001")
    save_package(pkg, make_events(), db_path=tmp_db)
    conn = sqlite3.connect(str(tmp_db))
    rows = conn.execute("SELECT * FROM agent_audit_events").fetchall()
    for row in rows:
        row_str = str(row)
        assert "echocardiography covered" not in row_str, "Full chunk text must not appear in audit records"
    conn.close()

@pytest.mark.implementation
def test_list_handoff_queue_excludes_errors(tmp_db):
    from case_summary_assistant.repository import save_package, list_handoff_queue
    save_package(make_handoff_package("Q-001", "HANDOFF_READY"), make_events(), db_path=tmp_db)
    save_package(make_handoff_package("Q-002", "PIPELINE_ERROR"), [], db_path=tmp_db)
    queue = list_handoff_queue(db_path=tmp_db)
    statuses = [q["status"] for q in queue]
    assert "PIPELINE_ERROR" not in statuses
    assert "HANDOFF_READY" in statuses
