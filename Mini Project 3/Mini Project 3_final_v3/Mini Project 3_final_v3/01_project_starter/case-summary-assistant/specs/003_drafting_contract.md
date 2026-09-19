# 003 — Drafting Contract

## Input
PriorAuthCase + list of RetrievedChunk objects

## Approved AI endpoint
Configured through the enterprise endpoint and deployment values in `.env`.
The integration must be swappable without changing `drafter.py`.

## Output: CaseSummary fields
- patient_context: dict — anonymized (no name, DOB, phone, email)
- approved_treatment: str — from case fields only, not invented
- cited_policy_sections: list[CitedSection] — each must trace to a retrieved chunk
- coverage_notes: str — grounded in chunk content only
- recommended_next_steps: list[str] — for care manager
- drafted_by: str — "DraftingAgent/v1.0"

## Grounding rule
The drafter MUST use only chunk text passed to it.
If a policy claim cannot be supported by a retrieved chunk, it must be omitted.
Raise DraftingError if the LLM response cannot be parsed into a valid CaseSummary.

## Anonymization
patient_context may include: age_band, diagnosis_category, procedure_type, urgency_level, payer_tier
patient_context must NOT include: name, date_of_birth, phone, email, address
