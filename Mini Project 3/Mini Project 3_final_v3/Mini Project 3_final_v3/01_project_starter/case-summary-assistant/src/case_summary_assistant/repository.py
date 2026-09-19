"""
SQLite repository for handoff cases and agent audit events.

Task 5: Implement save_package().

Rules:
- One transaction: handoff_case row + all agent_audit_events rows together.
- Audit records must not contain full summary text, patient PII, or raw chunk content.
- Triggers reject UPDATE and DELETE on agent_audit_events.

See: specs/006_persistence_and_audit.md
"""
from __future__ import annotations
import json, sqlite3, uuid
from datetime import datetime
from pathlib import Path

from case_summary_assistant.domain import HandoffPackage
from case_summary_assistant.llm_config import DATABASE_URL

DB_PATH = Path(DATABASE_URL)


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS handoff_cases (
            case_id              TEXT PRIMARY KEY,
            payer_id             TEXT NOT NULL,
            status               TEXT NOT NULL,
            summary_json         TEXT,
            confidence_score     REAL,
            retrieved_doc_sources TEXT,
            error_reason         TEXT,
            drafted_at           TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS agent_audit_events (
            event_id     TEXT PRIMARY KEY,
            case_id      TEXT NOT NULL REFERENCES handoff_cases(case_id),
            agent_name   TEXT NOT NULL,
            input_hash   TEXT NOT NULL,
            output_summary TEXT NOT NULL,
            executed_at  TEXT NOT NULL
        );

        CREATE TRIGGER IF NOT EXISTS no_update_agent_audit
        BEFORE UPDATE ON agent_audit_events
        BEGIN
            SELECT RAISE(ABORT, 'agent_audit_events is append-only: UPDATE forbidden');
        END;

        CREATE TRIGGER IF NOT EXISTS no_delete_agent_audit
        BEFORE DELETE ON agent_audit_events
        BEGIN
            SELECT RAISE(ABORT, 'agent_audit_events is append-only: DELETE forbidden');
        END;
    """)
    conn.commit()
    conn.close()


def find_by_case_id(case_id: str, db_path: Path = DB_PATH) -> dict | None:
    conn = get_connection(db_path)
    row = conn.execute("SELECT * FROM handoff_cases WHERE case_id=?", (case_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_audit_events(case_id: str, db_path: Path = DB_PATH) -> list[dict]:
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM agent_audit_events WHERE case_id=? ORDER BY executed_at", (case_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_cases(db_path: Path = DB_PATH) -> list[dict]:
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM handoff_cases ORDER BY drafted_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_handoff_queue(db_path: Path = DB_PATH) -> list[dict]:
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM handoff_cases WHERE status IN ('HANDOFF_READY','NEEDS_REVIEW') ORDER BY drafted_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_package(
    package: HandoffPackage,
    agent_events: list[dict],
    db_path: Path = DB_PATH,
) -> None:
    """
    Persist a HandoffPackage and its agent audit events atomically.

    Parameters
    ----------
    package : HandoffPackage
    agent_events : list[dict]
        One dict per executed agent: {agent_name, input_hash, output_summary}
    db_path : Path

    Rules
    -----
    - summary_json must NOT include patient name, DOB, phone, email.
    - output_summary in audit events must NOT include full text or PII.
    - Case and all audit events must be committed together or not at all.
    """
    # ── Mini Project Task 5: Implement save_package() ──────────────────────────
    init_db(db_path)

    safe_summary_json = None
    if package.summary is not None:
        patient_context = dict(package.summary.patient_context)
        for pii_field in ("name", "date_of_birth", "phone", "email", "address"):
            patient_context.pop(pii_field, None)
        safe_summary_json = json.dumps({
            "patient_context": patient_context,
            "approved_treatment": package.summary.approved_treatment,
            "cited_policy_sections": [
                {"source_doc": s.source_doc, "excerpt": s.excerpt, "relevance": s.relevance}
                for s in package.summary.cited_policy_sections
            ],
            "coverage_notes": package.summary.coverage_notes,
            "recommended_next_steps": package.summary.recommended_next_steps,
            "drafted_by": package.summary.drafted_by,
        })

    retrieved_doc_sources = ",".join(
        sorted({c.source_doc for c in package.retrieved_chunks})
    )

    # HandoffPackage carries no payer_id (it is not part of the anonymized
    # patient_context); the column is retained for future use.
    payer_id = ""

    conn = get_connection(db_path)
    try:
        conn.execute("BEGIN")
        conn.execute(
            """
            INSERT INTO handoff_cases
                (case_id, payer_id, status, summary_json, confidence_score,
                 retrieved_doc_sources, error_reason, drafted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                package.case_id,
                payer_id or "",
                package.status,
                safe_summary_json,
                package.confidence_score,
                retrieved_doc_sources,
                package.error_reason,
                package.drafted_at.isoformat(),
            ),
        )
        executed_at = datetime.utcnow().isoformat()
        for event in agent_events:
            conn.execute(
                """
                INSERT INTO agent_audit_events
                    (event_id, case_id, agent_name, input_hash, output_summary, executed_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    package.case_id,
                    event["agent_name"],
                    event["input_hash"],
                    event["output_summary"],
                    executed_at,
                ),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
