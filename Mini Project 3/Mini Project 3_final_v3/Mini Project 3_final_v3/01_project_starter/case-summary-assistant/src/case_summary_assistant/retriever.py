"""
RAG Retrieval Agent.

Task 1: Implement retrieve().

Rules:
- Query ChromaDB only. No LLM calls, no DB writes.
- Return RetrievedChunk objects sorted by similarity_score descending.
- Raise RetrievalError if the collection is missing or returns zero results.

IMPORTANT — Embedding policy:
- Use only the embedding endpoint or SDK approved by your organisation.
- Do NOT use DefaultEmbeddingFunction from ChromaDB.
- The embedding function is set at ingest time in scripts/ingest_policies.py.
- Plug in the approved enterprise embedding service there first.
- Ask your trainer/admin for the approved embedding endpoint or SDK.

See: specs/002_retrieval_contract.md
"""
from __future__ import annotations
from pathlib import Path

from case_summary_assistant.domain import PriorAuthCase, RetrievedChunk, RetrievalError
from case_summary_assistant.llm_config import CHROMA_PATH, CHROMA_COLLECTION, TOP_K_CHUNKS


def _get_collection():
    """Open and return the ChromaDB collection. Raise RetrievalError if not found."""
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(Path(CHROMA_PATH)))
        return client.get_collection(name=CHROMA_COLLECTION)
    except Exception as e:
        raise RetrievalError(
            f"ChromaDB collection '{CHROMA_COLLECTION}' not found at '{CHROMA_PATH}'. "
            "Run scripts/ingest_policies.py first."
        ) from e


def retrieve(case: PriorAuthCase, top_k: int = TOP_K_CHUNKS) -> list[RetrievedChunk]:
    """
    Query the policy vector store and return the top-k most relevant chunks.

    Parameters
    ----------
    case : PriorAuthCase
    top_k : int
        Number of chunks to retrieve (default from config).

    Returns
    -------
    list[RetrievedChunk]
        Sorted by similarity_score descending. At least 1 chunk.

    Raises
    ------
    RetrievalError
        If the collection is missing or returns zero results.
    """
    # ── Mini Project Task 1: Implement retrieve() ──────────────────────────────
    raise NotImplementedError(
        "Mini Project Task 1: Implement retrieve() in retriever.py.\n"
        "Steps:\n"
        "  1. Call _get_collection() to open the ChromaDB collection\n"
        "  2. Build query_text = case.icd10_prefix + ' ' + case.procedure_code + ' ' + case.payer_id\n"
        "  3. Call collection.query(query_texts=[query_text], n_results=top_k)\n"
        "  4. Map each result to RetrievedChunk(chunk_text, source_doc, page_number, similarity_score)\n"
        "     - documents[0][i] → chunk_text\n"
        "     - metadatas[0][i]['source'] → source_doc\n"
        "     - metadatas[0][i].get('page', 1) → page_number\n"
        "     - 1 - distances[0][i] → similarity_score (ChromaDB returns L2 distances)\n"
        "  5. Sort by similarity_score descending\n"
        "  6. Raise RetrievalError if result list is empty\n"
        "  7. Return the list\n"
        "See specs/002_retrieval_contract.md"
    )
