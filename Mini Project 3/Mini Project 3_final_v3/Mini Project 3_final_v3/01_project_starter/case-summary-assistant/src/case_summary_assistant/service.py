"""Application service — idempotency and coordination. Do not move pipeline logic here."""
from __future__ import annotations
from pathlib import Path
from case_summary_assistant.domain import PriorAuthCase, HandoffPackage
from case_summary_assistant import supervisor, repository


def evaluate(case: PriorAuthCase, db_path: Path = repository.DB_PATH) -> HandoffPackage:
    repository.init_db(db_path)
    existing = repository.find_by_case_id(case.case_id, db_path)
    if existing:
        events = repository.get_audit_events(case.case_id, db_path)
        return HandoffPackage(
            case_id=existing["case_id"],
            summary=None,
            retrieved_chunks=[],
            review_result=None,
            confidence_score=existing.get("confidence_score"),
            status=existing["status"],
            error_reason=existing.get("error_reason"),
            drafted_at=__import__("datetime").datetime.fromisoformat(existing["drafted_at"]),
            idempotent_replay=True,
        )
    package, agent_events = supervisor.run_pipeline(case)
    repository.save_package(package, agent_events, db_path)
    return package
