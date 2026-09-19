"""Shared fixtures."""
import pytest, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from case_summary_assistant.domain import (
    PriorAuthCase, RetrievedChunk, CaseSummary, CitedSection, ReviewResult
)

@pytest.fixture
def tier1_cardio_case():
    return PriorAuthCase(
        case_id="TEST-CARDIO-001", payer_id="PAY001",
        icd10_code="I25.10", icd10_prefix="I",
        procedure_code="93306", urgency="URGENT",
        age_band="31-55", diagnosis_category="Cardiovascular",
        procedure_type="Diagnostic imaging", payer_tier=1,
    )

@pytest.fixture
def tier3_oncology_case():
    return PriorAuthCase(
        case_id="TEST-ONCO-001", payer_id="PAY010",
        icd10_code="C34.10", icd10_prefix="C",
        procedure_code="61510", urgency="ROUTINE",
        age_band="over70", diagnosis_category="Oncology",
        procedure_type="Complex surgical", payer_tier=3,
    )

@pytest.fixture
def sample_chunks():
    return [
        RetrievedChunk(
            chunk_text="Cardiovascular diagnostic procedures including echocardiography (CPT 93306) are covered at 90% after deductible for Tier 1 members. Urgent cardiovascular cases receive expedited review.",
            source_doc="BlueCross_Tier1_General_Coverage_Policy.txt",
            page_number=2, similarity_score=0.92,
        ),
        RetrievedChunk(
            chunk_text="Prior authorization is required for all elective cardiovascular procedures. Coverage applies when the procedure is ordered by a network cardiologist.",
            source_doc="BlueCross_Tier1_General_Coverage_Policy.txt",
            page_number=2, similarity_score=0.88,
        ),
        RetrievedChunk(
            chunk_text="Tier 1 members receive preferred provider network access with the lowest out-of-pocket costs. URGENT requests are processed within 24 hours.",
            source_doc="BlueCross_Tier1_General_Coverage_Policy.txt",
            page_number=1, similarity_score=0.81,
        ),
    ]

@pytest.fixture
def grounded_summary(sample_chunks):
    return CaseSummary(
        patient_context={"age_band": "31-55", "diagnosis_category": "Cardiovascular", "urgency_level": "URGENT", "payer_tier": 1},
        approved_treatment="Echocardiography (CPT 93306)",
        cited_policy_sections=[
            CitedSection(
                source_doc="BlueCross_Tier1_General_Coverage_Policy.txt",
                excerpt="echocardiography (CPT 93306) are covered at 90% after deductible for Tier 1 members",
                relevance="Confirms procedure coverage at 90%",
            )
        ],
        coverage_notes="Covered at 90% in-network after deductible. Expedited review for URGENT cases.",
        recommended_next_steps=["Schedule echocardiography with network cardiologist", "Verify deductible status"],
    )

@pytest.fixture
def ungrounded_summary():
    return CaseSummary(
        patient_context={"age_band": "over70", "diagnosis_category": "Oncology"},
        approved_treatment="Craniotomy (CPT 61510)",
        cited_policy_sections=[
            CitedSection(
                source_doc="SomePolicy.txt",
                excerpt="this text does not appear in any retrieved chunk at all",
                relevance="Invented claim",
            )
        ],
        coverage_notes="Some invented coverage note.",
        recommended_next_steps=["Proceed with surgery"],
    )

@pytest.fixture
def tmp_db(tmp_path):
    db = tmp_path / "test_cases.db"
    from case_summary_assistant.repository import init_db
    init_db(db)
    return db
