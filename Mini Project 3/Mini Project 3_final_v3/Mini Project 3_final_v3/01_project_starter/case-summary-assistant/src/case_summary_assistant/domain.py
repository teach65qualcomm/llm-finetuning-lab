"""Typed domain objects for the Case-Summary Drafting Assistant."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class PriorAuthCase:
    case_id: str
    payer_id: str
    icd10_code: str
    icd10_prefix: str
    procedure_code: str
    urgency: str           # ROUTINE | URGENT | STAT
    age_band: str          # under18 | 18-30 | 31-55 | 56-70 | over70
    diagnosis_category: str
    procedure_type: str
    payer_tier: int        # 1 | 2 | 3


@dataclass
class RetrievedChunk:
    chunk_text: str
    source_doc: str
    page_number: int
    similarity_score: float


@dataclass
class CitedSection:
    source_doc: str
    excerpt: str
    relevance: str  # one-line note on why this section applies


@dataclass
class CaseSummary:
    patient_context: dict
    approved_treatment: str
    cited_policy_sections: list[CitedSection]
    coverage_notes: str
    recommended_next_steps: list[str]
    drafted_by: str = "DraftingAgent/v1.0"


@dataclass
class ReviewResult:
    confidence_score: float
    flagged_gaps: list[str]
    recommendation: str   # APPROVE | FLAG_FOR_HUMAN


@dataclass
class HandoffPackage:
    case_id: str
    summary: Optional[CaseSummary]
    retrieved_chunks: list[RetrievedChunk]
    review_result: Optional[ReviewResult]
    confidence_score: Optional[float]
    status: str            # HANDOFF_READY | NEEDS_REVIEW | PIPELINE_ERROR
    error_reason: Optional[str]
    drafted_at: datetime
    idempotent_replay: bool = False


class RetrievalError(Exception):
    """Raised when the vector store cannot return results."""
    pass


class DraftingError(Exception):
    """Raised when the LLM response cannot be parsed into a valid CaseSummary."""
    pass
