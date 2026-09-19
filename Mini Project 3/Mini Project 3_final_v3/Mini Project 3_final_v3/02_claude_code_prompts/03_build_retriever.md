# Prompt 3 — Build the RAG Retrieval Agent (Task 1)

## Embedding policy
Use only the embedding endpoint or SDK approved by your organisation.
Do NOT use DefaultEmbeddingFunction from ChromaDB.
Do not add an unapproved embedding provider or local runtime.
Ask your trainer/admin for the approved embedding endpoint or SDK.
Plug it into the CompanyEmbeddingFunction stub in scripts/ingest_policies.py before running ingest.

1. Run: `python -m pytest tests/test_retriever.py -m implementation -q` — observe failures
2. Read specs/002_retrieval_contract.md carefully
3. Implement retrieve() in retriever.py:
   - Build query: icd10_prefix + " " + procedure_code + " " + payer_id
   - Call collection.query(query_texts=[query_text], n_results=top_k)
   - Map results to RetrievedChunk objects
   - Sort by similarity_score descending
   - Raise RetrievalError if zero results
4. Run tests again — all implementation tests in test_retriever.py must pass

Do not call the LLM from retriever.py. Do not write to the database from retriever.py.
