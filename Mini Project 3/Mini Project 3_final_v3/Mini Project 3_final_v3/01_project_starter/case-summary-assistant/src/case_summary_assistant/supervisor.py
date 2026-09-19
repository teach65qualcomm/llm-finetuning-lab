"""
Supervisor Agent — orchestrates all sub-agents.

Task 4: Implement run_pipeline().

Stage sequence (fixed):
  1. RETRIEVAL        — retriever.retrieve(case)
  2. DRAFTING         — drafter.draft(case, chunks)
  3. REVIEW           — reviewer.review(summary, chunks)
  4. HANDOFF_ASSEMBLY — build HandoffPackage

Rules:
- Stop at any sub-agent exception → PIPELINE_ERROR
- APPROVE → HANDOFF_READY; FLAG_FOR_HUMAN → NEEDS_REVIEW
- Never send a message or contact any external system.

See: specs/005_supervisor_contract.md
"""
from __future__ import annotations
import hashlib, json
from datetime import datetime

from case_summary_assistant.domain import (
    PriorAuthCase, HandoffPackage, RetrievedChunk, CaseSummary, ReviewResult
)
from case_summary_assistant import retriever, drafter, reviewer


def _input_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def run_pipeline(case: PriorAuthCase) -> tuple[HandoffPackage, list[dict]]:
    """
    Run the full multi-agent pipeline for a prior-auth case.

    Parameters
    ----------
    case : PriorAuthCase

    Returns
    -------
    tuple[HandoffPackage, list[dict]]
        The HandoffPackage and a list of agent audit event dicts
        (one per executed stage).
    """
    # ── Mini Project Task 4: Implement run_pipeline() ──────────────────────────
    agent_events: list[dict] = []
    drafted_at = datetime.utcnow()

    def _pipeline_error(e: Exception) -> HandoffPackage:
        return HandoffPackage(
            case_id=case.case_id, summary=None, retrieved_chunks=[],
            review_result=None, confidence_score=None, status="PIPELINE_ERROR",
            error_reason=str(e), drafted_at=drafted_at,
        )

    # Stage 1 — RETRIEVAL
    try:
        chunks = retriever.retrieve(case)
        agent_events.append({
            "agent_name": "RETRIEVER",
            "input_hash": _input_hash(case.case_id),
            "output_summary": f"{len(chunks)} chunks retrieved",
        })
    except Exception as e:
        return _pipeline_error(e), agent_events

    # Stage 2 — DRAFTING
    try:
        summary = drafter.draft(case, chunks)
        agent_events.append({
            "agent_name": "DRAFTER",
            "input_hash": _input_hash(case.case_id),
            "output_summary": f"{len(summary.cited_policy_sections)} cited sections",
        })
    except Exception as e:
        return _pipeline_error(e), agent_events

    # Stage 3 — REVIEW
    try:
        review_result = reviewer.review(summary, chunks)
        agent_events.append({
            "agent_name": "REVIEWER",
            "input_hash": _input_hash(case.case_id),
            "output_summary": f"confidence={review_result.confidence_score:.2f}",
        })
    except Exception as e:
        return _pipeline_error(e), agent_events

    # Stage 4 — HANDOFF_ASSEMBLY
    status = "HANDOFF_READY" if review_result.recommendation == "APPROVE" else "NEEDS_REVIEW"
    agent_events.append({
        "agent_name": "HANDOFF_ASSEMBLY",
        "input_hash": _input_hash(case.case_id),
        "output_summary": status,
    })

    package = HandoffPackage(
        case_id=case.case_id, summary=summary, retrieved_chunks=chunks,
        review_result=review_result, confidence_score=review_result.confidence_score,
        status=status, error_reason=None, drafted_at=drafted_at,
    )
    return package, agent_events
