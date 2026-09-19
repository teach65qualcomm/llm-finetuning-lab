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
        from case_summary_assistant.embeddings import CompanyEmbeddingFunction
        client = chromadb.PersistentClient(path=str(Path(CHROMA_PATH)))
        return client.get_collection(name=CHROMA_COLLECTION, embedding_function=CompanyEmbeddingFunction())
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
    collection = _get_collection()
    query_text = f"{case.icd10_prefix} {case.procedure_code} {case.payer_id}"

    results = collection.query(query_texts=[query_text], n_results=top_k)

    documents = results.get("documents") or [[]]
    metadatas = results.get("metadatas") or [[]]
    distances = results.get("distances") or [[]]

    if not documents or not documents[0]:
        raise RetrievalError(
            f"No results returned from ChromaDB collection '{CHROMA_COLLECTION}' "
            f"for query '{query_text}'."
        )

    chunks: list[RetrievedChunk] = []
    for doc, meta, dist in zip(documents[0], metadatas[0], distances[0]):
        chunks.append(
            RetrievedChunk(
                chunk_text=doc,
                source_doc=meta["source"],
                page_number=meta.get("page", 1),
                similarity_score=1 - dist,
            )
        )

    chunks.sort(key=lambda c: c.similarity_score, reverse=True)
    return chunks
