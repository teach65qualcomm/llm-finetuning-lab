# Healthcare Safety Rules

## What this service MAY do
- Query ChromaDB for policy document chunks relevant to a case
- Draft a structured case summary grounded in retrieved chunks
- Quality-check the summary for citation grounding
- Stage a handoff package (HANDOFF_READY or NEEDS_REVIEW) for the care manager
- Store cases and audit events in SQLite

## What this service must NEVER do
- Send any message, email, or notification to any party
- Contact any external system (insurer, EMR, patient portal)
- Make a coverage, clinical, or payment decision
- Output a summary containing patient name, date of birth, phone, or email
- Invent policy content not present in the retrieved chunks

## Anonymization rules for patient_context
ALLOWED: age_band, diagnosis_category, procedure_type, urgency_level, payer_tier
FORBIDDEN: patient name, date_of_birth, phone, email, address, patient_id in readable form

## Safe audit evidence
ALLOWED: confidence_score, status, agent_name, retrieved_doc_sources (filenames), input_hash
FORBIDDEN: full summary text, full chunk text, patient name, DOB, phone, email
