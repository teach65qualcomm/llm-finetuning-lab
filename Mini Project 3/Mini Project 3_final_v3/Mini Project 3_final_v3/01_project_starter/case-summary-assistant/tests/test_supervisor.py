"""Tests for the supervisor agent — Task 4."""
import pytest
from unittest.mock import patch, MagicMock
from case_summary_assistant.domain import HandoffPackage, RetrievalError

@pytest.mark.baseline
def test_supervisor_importable():
    from case_summary_assistant import supervisor
    assert hasattr(supervisor, "run_pipeline")

@pytest.mark.baseline
def test_handoff_package_importable():
    assert HandoffPackage is not None

@pytest.mark.implementation
def test_pipeline_returns_tuple(tier1_cardio_case, sample_chunks, grounded_summary):
    from case_summary_assistant import supervisor
    from case_summary_assistant.domain import ReviewResult
    mock_review = ReviewResult(confidence_score=0.90, flagged_gaps=[], recommendation="APPROVE")
    with patch("case_summary_assistant.supervisor.retriever") as mr, \
         patch("case_summary_assistant.supervisor.drafter") as md, \
         patch("case_summary_assistant.supervisor.reviewer") as mrv:
        mr.retrieve.return_value = sample_chunks
        md.draft.return_value = grounded_summary
        mrv.review.return_value = mock_review
        result, events = supervisor.run_pipeline(tier1_cardio_case)
    assert isinstance(result, HandoffPackage)
    assert isinstance(events, list)

@pytest.mark.implementation
def test_approve_gives_handoff_ready(tier1_cardio_case, sample_chunks, grounded_summary):
    from case_summary_assistant import supervisor
    from case_summary_assistant.domain import ReviewResult
    mock_review = ReviewResult(confidence_score=0.90, flagged_gaps=[], recommendation="APPROVE")
    with patch("case_summary_assistant.supervisor.retriever") as mr, \
         patch("case_summary_assistant.supervisor.drafter") as md, \
         patch("case_summary_assistant.supervisor.reviewer") as mrv:
        mr.retrieve.return_value = sample_chunks
        md.draft.return_value = grounded_summary
        mrv.review.return_value = mock_review
        result, _ = supervisor.run_pipeline(tier1_cardio_case)
    assert result.status == "HANDOFF_READY"

@pytest.mark.implementation
def test_flag_gives_needs_review(tier1_cardio_case, sample_chunks, grounded_summary):
    from case_summary_assistant import supervisor
    from case_summary_assistant.domain import ReviewResult
    mock_review = ReviewResult(confidence_score=0.50, flagged_gaps=["Gap 1"], recommendation="FLAG_FOR_HUMAN")
    with patch("case_summary_assistant.supervisor.retriever") as mr, \
         patch("case_summary_assistant.supervisor.drafter") as md, \
         patch("case_summary_assistant.supervisor.reviewer") as mrv:
        mr.retrieve.return_value = sample_chunks
        md.draft.return_value = grounded_summary
        mrv.review.return_value = mock_review
        result, _ = supervisor.run_pipeline(tier1_cardio_case)
    assert result.status == "NEEDS_REVIEW"

@pytest.mark.implementation
def test_retrieval_error_gives_pipeline_error(tier1_cardio_case):
    from case_summary_assistant import supervisor
    with patch("case_summary_assistant.supervisor.retriever") as mr:
        mr.retrieve.side_effect = RetrievalError("No chunks found")
        result, events = supervisor.run_pipeline(tier1_cardio_case)
    assert result.status == "PIPELINE_ERROR"
    assert result.error_reason is not None

@pytest.mark.implementation
def test_four_agent_events_on_success(tier1_cardio_case, sample_chunks, grounded_summary):
    from case_summary_assistant import supervisor
    from case_summary_assistant.domain import ReviewResult
    mock_review = ReviewResult(confidence_score=0.90, flagged_gaps=[], recommendation="APPROVE")
    with patch("case_summary_assistant.supervisor.retriever") as mr, \
         patch("case_summary_assistant.supervisor.drafter") as md, \
         patch("case_summary_assistant.supervisor.reviewer") as mrv:
        mr.retrieve.return_value = sample_chunks
        md.draft.return_value = grounded_summary
        mrv.review.return_value = mock_review
        _, events = supervisor.run_pipeline(tier1_cardio_case)
    assert len(events) == 4

@pytest.mark.implementation
def test_one_event_on_retrieval_failure(tier1_cardio_case):
    from case_summary_assistant import supervisor
    with patch("case_summary_assistant.supervisor.retriever") as mr:
        mr.retrieve.side_effect = RetrievalError("Empty")
        _, events = supervisor.run_pipeline(tier1_cardio_case)
    assert len(events) == 1
    assert events[0]["agent_name"] == "RETRIEVER"

@pytest.mark.implementation
def test_handoff_package_has_case_id(tier1_cardio_case, sample_chunks, grounded_summary):
    from case_summary_assistant import supervisor
    from case_summary_assistant.domain import ReviewResult
    mock_review = ReviewResult(confidence_score=0.90, flagged_gaps=[], recommendation="APPROVE")
    with patch("case_summary_assistant.supervisor.retriever") as mr, \
         patch("case_summary_assistant.supervisor.drafter") as md, \
         patch("case_summary_assistant.supervisor.reviewer") as mrv:
        mr.retrieve.return_value = sample_chunks
        md.draft.return_value = grounded_summary
        mrv.review.return_value = mock_review
        result, _ = supervisor.run_pipeline(tier1_cardio_case)
    assert result.case_id == tier1_cardio_case.case_id
