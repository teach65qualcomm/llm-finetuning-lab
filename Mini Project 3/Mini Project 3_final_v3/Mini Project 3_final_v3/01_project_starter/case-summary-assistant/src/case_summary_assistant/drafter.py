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
    raise NotImplementedError(
        "Mini Project Task 2: Implement draft() in drafter.py.\n"
        "Steps:\n"
        "  1. Call get_llm_client() to get the configured LLM client\n"
        "  2. Build the prompt using DRAFTING_PROMPT_TEMPLATE.format(\n"
        "       case_context=_build_case_context(case),\n"
        "       chunks=_build_chunks_context(chunks)\n"
        "     )\n"
        "  3. Call the LLM using the OpenAI SDK client shape:\n"
        "       response = client.chat.completions.create(\n"
        "           model=ENTERPRISE_LLM_DEPLOYMENT,\n"
        "           messages=[{'role': 'user', 'content': prompt}],\n"
        "           response_format={'type': 'json_object'}\n"
        "       )\n"
        "  4. Read the response as: response.choices[0].message.content\n"
        "     This matches the mock in tests/test_drafter.py.\n"
        "  5. Parse the content string as JSON\n"
        "  6. Map to CaseSummary — wrap each cited section as CitedSection object\n"
        "  7. Raise DraftingError if parsing fails or required fields are missing\n"
        "  8. Verify patient_context does NOT contain name, date_of_birth, phone, email\n"
        "     If any are present, remove them before returning\n"
        "See specs/003_drafting_contract.md"
    )
