"""Tests for the drafting agent — Task 2."""
import pytest
from unittest.mock import patch, MagicMock
from case_summary_assistant.domain import CaseSummary, DraftingError

MOCK_LLM_RESPONSE = {
    "patient_context": {"age_band": "31-55", "diagnosis_category": "Cardiovascular", "urgency_level": "URGENT", "payer_tier": 1},
    "approved_treatment": "Echocardiography (CPT 93306)",
    "cited_policy_sections": [
        {"source_doc": "BlueCross_Tier1_General_Coverage_Policy.txt",
         "excerpt": "echocardiography (CPT 93306) are covered at 90% after deductible for Tier 1 members",
         "relevance": "Confirms procedure coverage at 90%"}
    ],
    "coverage_notes": "Covered at 90% in-network after deductible.",
    "recommended_next_steps": ["Schedule with network cardiologist", "Verify deductible status"],
}

import json

def make_mock_client(response_dict):
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.message.content = json.dumps(response_dict)
    mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_msg])
    return mock_client

@pytest.mark.baseline
def test_drafter_importable():
    from case_summary_assistant import drafter
    assert hasattr(drafter, "draft")

@pytest.mark.baseline
def test_drafting_error_importable():
    assert DraftingError is not None

@pytest.mark.implementation
def test_draft_returns_case_summary(tier1_cardio_case, sample_chunks):
    from case_summary_assistant import drafter
    with patch("case_summary_assistant.drafter.get_llm_client", return_value=make_mock_client(MOCK_LLM_RESPONSE)):
        result = drafter.draft(tier1_cardio_case, sample_chunks)
    assert isinstance(result, CaseSummary)

@pytest.mark.implementation
def test_patient_context_excludes_pii(tier1_cardio_case, sample_chunks):
    from case_summary_assistant import drafter
    with patch("case_summary_assistant.drafter.get_llm_client", return_value=make_mock_client(MOCK_LLM_RESPONSE)):
        result = drafter.draft(tier1_cardio_case, sample_chunks)
    forbidden = {"name", "date_of_birth", "phone", "email", "address"}
    for key in result.patient_context.keys():
        assert key not in forbidden, f"Forbidden PII field '{key}' found in patient_context"

@pytest.mark.implementation
def test_draft_has_cited_sections(tier1_cardio_case, sample_chunks):
    from case_summary_assistant import drafter
    with patch("case_summary_assistant.drafter.get_llm_client", return_value=make_mock_client(MOCK_LLM_RESPONSE)):
        result = drafter.draft(tier1_cardio_case, sample_chunks)
    assert len(result.cited_policy_sections) >= 1

@pytest.mark.implementation
def test_drafting_error_on_bad_llm_response(tier1_cardio_case, sample_chunks):
    from case_summary_assistant import drafter
    bad_client = MagicMock()
    bad_msg = MagicMock()
    bad_msg.message.content = "not valid json {{{{"
    bad_client.chat.completions.create.return_value = MagicMock(choices=[bad_msg])
    with patch("case_summary_assistant.drafter.get_llm_client", return_value=bad_client):
        with pytest.raises(DraftingError):
            drafter.draft(tier1_cardio_case, sample_chunks)

@pytest.mark.implementation
def test_drafted_by_field(tier1_cardio_case, sample_chunks):
    from case_summary_assistant import drafter
    with patch("case_summary_assistant.drafter.get_llm_client", return_value=make_mock_client(MOCK_LLM_RESPONSE)):
        result = drafter.draft(tier1_cardio_case, sample_chunks)
    assert "DraftingAgent" in result.drafted_by
