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
    raise NotImplementedError(
        "Mini Project Task 3: Implement review() in reviewer.py.\n"
        "Steps:\n"
        "  1. Get all chunk texts as a single lowercase string for matching:\n"
        "     all_chunk_text = ' '.join(c.chunk_text.lower().strip() for c in chunks)\n"
        "  2. For each section in summary.cited_policy_sections:\n"
        "     - excerpt = section.excerpt.lower().strip()\n"
        "     - If excerpt in all_chunk_text: verified += 1\n"
        "     - Else: add to flagged_gaps with message 'Citation not found in retrieved chunks: {excerpt[:80]}'\n"
        "  3. total = len(summary.cited_policy_sections)\n"
        "     confidence_score = verified / total if total > 0 else 1.0\n"
        "  4. recommendation = 'FLAG_FOR_HUMAN' if confidence_score < CONFIDENCE_THRESHOLD else 'APPROVE'\n"
        "  5. Return ReviewResult(confidence_score=confidence_score, flagged_gaps=flagged_gaps, recommendation=recommendation)\n"
        "See specs/004_review_contract.md"
    )
