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
    raise NotImplementedError(
        "Mini Project Task 4: Implement run_pipeline() in supervisor.py.\n"
        "Steps:\n"
        "  agent_events = []\n"
        "  drafted_at = datetime.utcnow()\n"
        "\n"
        "  Stage 1 — RETRIEVAL:\n"
        "    try:\n"
        "      chunks = retriever.retrieve(case)\n"
        "      agent_events.append({'agent_name': 'RETRIEVER', 'input_hash': _input_hash(case.case_id),\n"
        "        'output_summary': f'{len(chunks)} chunks retrieved'})\n"
        "    except Exception as e:\n"
        "      return HandoffPackage(case_id=case.case_id, summary=None, retrieved_chunks=[],\n"
        "        review_result=None, confidence_score=None, status='PIPELINE_ERROR',\n"
        "        error_reason=str(e), drafted_at=drafted_at), agent_events\n"
        "\n"
        "  Stage 2 — DRAFTING (same pattern, call drafter.draft(case, chunks))\n"
        "  Stage 3 — REVIEW (same pattern, call reviewer.review(summary, chunks))\n"
        "\n"
        "  Stage 4 — HANDOFF_ASSEMBLY:\n"
        "    status = 'HANDOFF_READY' if review_result.recommendation == 'APPROVE' else 'NEEDS_REVIEW'\n"
        "    agent_events.append({'agent_name': 'HANDOFF_ASSEMBLY', ...})\n"
        "    return HandoffPackage(case_id, summary, chunks, review_result,\n"
        "      confidence_score=review_result.confidence_score, status=status,\n"
        "      error_reason=None, drafted_at=drafted_at), agent_events\n"
        "See specs/005_supervisor_contract.md"
    )
