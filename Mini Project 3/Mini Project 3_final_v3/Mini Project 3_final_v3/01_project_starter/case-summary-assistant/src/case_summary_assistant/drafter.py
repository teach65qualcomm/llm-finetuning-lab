"""
Drafting Agent.

Task 2: Implement draft().

Rules:
- Use LLM via get_llm_client() from llm_config.py.
- Call the LLM using the OpenAI SDK client shape:
    client.chat.completions.create(model=..., messages=[...], response_format=...)
  Read the response as: response.choices[0].message.content
  This matches the mock used in tests/test_drafter.py.
- Use ONLY the retrieved chunk text — never invent policy content.
- Patient context must exclude name, DOB, phone, email.
- Raise DraftingError if response cannot be parsed into CaseSummary.

See: specs/003_drafting_contract.md
"""
from __future__ import annotations
import json

from case_summary_assistant.domain import (
    PriorAuthCase, RetrievedChunk, CaseSummary, CitedSection, DraftingError
)
from case_summary_assistant.llm_config import (
    get_llm_client, ENTERPRISE_LLM_DEPLOYMENT, DRAFTING_PROMPT_TEMPLATE
)


def _build_case_context(case: PriorAuthCase) -> str:
    """Build anonymized case context string for the prompt."""
    return (
        f"Age band: {case.age_band}\n"
        f"Diagnosis category: {case.diagnosis_category}\n"
        f"Procedure type: {case.procedure_type}\n"
        f"Urgency level: {case.urgency}\n"
        f"Payer tier: {case.payer_tier}\n"
        f"ICD-10 prefix: {case.icd10_prefix}\n"
        f"Procedure code: {case.procedure_code}"
    )


def _build_chunks_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks for the prompt."""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Chunk {i} | Source: {chunk.source_doc} | Page: {chunk.page_number} "
            f"| Score: {chunk.similarity_score:.3f}]\n{chunk.chunk_text}"
        )
    return "\n\n".join(parts)


def draft(case: PriorAuthCase, chunks: list[RetrievedChunk]) -> CaseSummary:
    """
    Draft a structured CaseSummary grounded in the retrieved policy chunks.

    Parameters
    ----------
    case : PriorAuthCase
    chunks : list[RetrievedChunk]
        Retrieved policy chunks from the retrieval agent.

    Returns
    -------
    CaseSummary

    Raises
    ------
    DraftingError
        If the LLM response cannot be parsed into a valid CaseSummary.
    """
    # ── Mini Project Task 2: Implement draft() ────────────────────────────────
    client = get_llm_client()
    prompt = DRAFTING_PROMPT_TEMPLATE.format(
        case_context=_build_case_context(case),
        chunks=_build_chunks_context(chunks),
    )

    response = client.chat.completions.create(
        model=ENTERPRISE_LLM_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content

    try:
        data = json.loads(content)
    except (TypeError, json.JSONDecodeError) as e:
        raise DraftingError(f"LLM response is not valid JSON: {e}") from e

    required_fields = {
        "patient_context", "approved_treatment", "cited_policy_sections",
        "coverage_notes", "recommended_next_steps",
    }
    missing = required_fields - data.keys()
    if missing:
        raise DraftingError(f"LLM response missing required fields: {sorted(missing)}")

    patient_context = dict(data["patient_context"])
    for pii_field in ("name", "date_of_birth", "phone", "email", "address"):
        patient_context.pop(pii_field, None)

    try:
        cited_sections = [
            CitedSection(
                source_doc=section["source_doc"],
                excerpt=section["excerpt"],
                relevance=section["relevance"],
            )
            for section in data["cited_policy_sections"]
        ]
    except (KeyError, TypeError) as e:
        raise DraftingError(f"LLM response has malformed cited_policy_sections: {e}") from e

    return CaseSummary(
        patient_context=patient_context,
        approved_treatment=data["approved_treatment"],
        cited_policy_sections=cited_sections,
        coverage_notes=data["coverage_notes"],
        recommended_next_steps=list(data["recommended_next_steps"]),
    )
