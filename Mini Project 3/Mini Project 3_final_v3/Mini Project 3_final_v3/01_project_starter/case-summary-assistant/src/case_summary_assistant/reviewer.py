"""
Review Agent — citation verification and confidence scoring.

Task 3: Implement review().

Rules:
- Pure Python only. No LLM calls, no DB access.
- Verify citations by substring match (case-insensitive, stripped).
- confidence_score = verified / total (1.0 if no citations).
- FLAG_FOR_HUMAN if confidence_score < CONFIDENCE_THRESHOLD.

See: specs/004_review_contract.md
"""
from __future__ import annotations
from case_summary_assistant.domain import CaseSummary, RetrievedChunk, ReviewResult
from case_summary_assistant.llm_config import CONFIDENCE_THRESHOLD


def review(summary: CaseSummary, chunks: list[RetrievedChunk]) -> ReviewResult:
    """
    Quality-check the drafted summary for citation grounding.

    Parameters
    ----------
    summary : CaseSummary
        The drafted summary from the drafting agent.
    chunks : list[RetrievedChunk]
        The same chunks that were passed to the drafter.

    Returns
    -------
    ReviewResult
        confidence_score, flagged_gaps, recommendation (APPROVE | FLAG_FOR_HUMAN)
    """
    # ── Mini Project Task 3: Implement review() ───────────────────────────────
    all_chunk_text = " ".join(c.chunk_text.lower().strip() for c in chunks)

    verified = 0
    flagged_gaps: list[str] = []
    for section in summary.cited_policy_sections:
        excerpt = section.excerpt.lower().strip()
        if excerpt in all_chunk_text:
            verified += 1
        else:
            flagged_gaps.append(f"Citation not found in retrieved chunks: {excerpt[:80]}")

    total = len(summary.cited_policy_sections)
    confidence_score = verified / total if total > 0 else 1.0
    recommendation = "FLAG_FOR_HUMAN" if confidence_score < CONFIDENCE_THRESHOLD else "APPROVE"

    return ReviewResult(
        confidence_score=confidence_score,
        flagged_gaps=flagged_gaps,
        recommendation=recommendation,
    )
