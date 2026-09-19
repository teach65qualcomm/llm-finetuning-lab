# 002 — Retrieval Contract

## Input
A PriorAuthCase object with: case_id, payer_id, icd10_prefix, procedure_code, urgency

## Query construction
Build semantic query from: icd10_prefix + " " + procedure_code + " " + payer_id

## Output
List of RetrievedChunk objects, sorted by similarity_score descending.
Minimum: 1 chunk. Maximum: top_k (default 5, configurable).

## RetrievedChunk fields
- chunk_text: str — the policy document text
- source_doc: str — filename of the source policy document
- page_number: int — page within the source document
- similarity_score: float — 0.0 to 1.0

## Error handling
Raise RetrievalError if:
- The ChromaDB collection does not exist
- The vector store returns zero results for any valid query

## Constraints
- Do NOT call the LLM from the retriever
- Do NOT write to the database from the retriever
- Do NOT re-ingest documents on each call
