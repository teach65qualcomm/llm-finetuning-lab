"""Tests for the review agent — Task 3."""
import pytest
from case_summary_assistant.domain import ReviewResult

@pytest.mark.baseline
def test_reviewer_importable():
    from case_summary_assistant import reviewer
    assert hasattr(reviewer, "review")

@pytest.mark.baseline
def test_review_result_importable():
    assert ReviewResult is not None

@pytest.mark.implementation
def test_review_returns_review_result(grounded_summary, sample_chunks):
    from case_summary_assistant.reviewer import review
    result = review(grounded_summary, sample_chunks)
    assert isinstance(result, ReviewResult)

@pytest.mark.implementation
def test_all_verified_citations_score_1(grounded_summary, sample_chunks):
    from case_summary_assistant.reviewer import review
    result = review(grounded_summary, sample_chunks)
    assert result.confidence_score == 1.0
    assert result.recommendation == "APPROVE"

@pytest.mark.implementation
def test_unverified_citation_lowers_score(ungrounded_summary, sample_chunks):
    from case_summary_assistant.reviewer import review
    result = review(ungrounded_summary, sample_chunks)
    assert result.confidence_score < 1.0

@pytest.mark.implementation
def test_low_confidence_triggers_flag_for_human(ungrounded_summary, sample_chunks):
    from case_summary_assistant.reviewer import review
    result = review(ungrounded_summary, sample_chunks)
    assert result.recommendation == "FLAG_FOR_HUMAN"

@pytest.mark.implementation
def test_flagged_gaps_populated_on_unverified(ungrounded_summary, sample_chunks):
    from case_summary_assistant.reviewer import review
    result = review(ungrounded_summary, sample_chunks)
    assert len(result.flagged_gaps) >= 1

@pytest.mark.implementation
def test_empty_citations_gives_full_confidence_and_approve(grounded_summary, sample_chunks):
    """
    A summary with no cited_policy_sections has no unverified claims.
    confidence_score = 1.0 and recommendation = APPROVE.
    The absence of citations is not a failure — the reviewer only checks
    citations that are present. See specs/004_review_contract.md.
    """
    from case_summary_assistant.domain import CaseSummary
    from case_summary_assistant.reviewer import review
    empty_summary = CaseSummary(
        patient_context={}, approved_treatment="Test",
        cited_policy_sections=[], coverage_notes="", recommended_next_steps=[],
    )
    result = review(empty_summary, sample_chunks)
    assert result.confidence_score == 1.0
    assert result.recommendation == "APPROVE"

@pytest.mark.implementation
def test_confidence_score_in_range(grounded_summary, sample_chunks):
    from case_summary_assistant.reviewer import review
    result = review(grounded_summary, sample_chunks)
    assert 0.0 <= result.confidence_score <= 1.0

@pytest.mark.implementation
def test_below_threshold_always_flag(sample_chunks):
    from case_summary_assistant.domain import CaseSummary, CitedSection
    from case_summary_assistant.reviewer import review
    bad_summary = CaseSummary(
        patient_context={}, approved_treatment="X",
        cited_policy_sections=[
            CitedSection(source_doc="X.txt", excerpt="XXXXNOTFOUNDXXXX", relevance="bad"),
            CitedSection(source_doc="Y.txt", excerpt="YYYYNOTFOUNDYYYY", relevance="bad"),
        ],
        coverage_notes="", recommended_next_steps=[],
    )
    result = review(bad_summary, sample_chunks)
    assert result.recommendation == "FLAG_FOR_HUMAN"
    assert result.confidence_score < 0.70
