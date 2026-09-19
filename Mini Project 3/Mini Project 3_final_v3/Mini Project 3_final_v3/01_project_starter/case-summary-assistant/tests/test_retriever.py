"""Tests for the RAG retrieval agent — Task 1."""
import pytest
from case_summary_assistant.domain import RetrievedChunk, RetrievalError

@pytest.mark.baseline
def test_retriever_importable():
    from case_summary_assistant import retriever
    assert hasattr(retriever, "retrieve")

@pytest.mark.baseline
def test_retrieved_chunk_importable():
    assert RetrievedChunk is not None

@pytest.mark.baseline
def test_retrieval_error_importable():
    assert RetrievalError is not None

@pytest.mark.implementation
def test_retrieve_returns_list(tier1_cardio_case):
    from case_summary_assistant.retriever import retrieve
    chunks = retrieve(tier1_cardio_case)
    assert isinstance(chunks, list)

@pytest.mark.implementation
def test_retrieve_returns_at_least_one_chunk(tier1_cardio_case):
    from case_summary_assistant.retriever import retrieve
    chunks = retrieve(tier1_cardio_case)
    assert len(chunks) >= 1

@pytest.mark.implementation
def test_retrieve_returns_chunk_objects(tier1_cardio_case):
    from case_summary_assistant.retriever import retrieve
    chunks = retrieve(tier1_cardio_case)
    for c in chunks:
        assert isinstance(c, RetrievedChunk)

@pytest.mark.implementation
def test_chunks_sorted_by_similarity_descending(tier1_cardio_case):
    from case_summary_assistant.retriever import retrieve
    chunks = retrieve(tier1_cardio_case)
    scores = [c.similarity_score for c in chunks]
    assert scores == sorted(scores, reverse=True), "Chunks must be sorted by similarity_score descending"

@pytest.mark.implementation
def test_chunks_have_source_doc(tier1_cardio_case):
    from case_summary_assistant.retriever import retrieve
    chunks = retrieve(tier1_cardio_case)
    for c in chunks:
        assert c.source_doc, "Each chunk must have a source_doc"
        assert c.source_doc.endswith(".txt"), "source_doc must be a .txt filename"

@pytest.mark.implementation
def test_chunks_have_page_number(tier1_cardio_case):
    from case_summary_assistant.retriever import retrieve
    chunks = retrieve(tier1_cardio_case)
    for c in chunks:
        assert isinstance(c.page_number, int) and c.page_number >= 1

@pytest.mark.implementation
def test_empty_collection_raises_retrieval_error(monkeypatch):
    from case_summary_assistant import retriever
    from case_summary_assistant.domain import PriorAuthCase
    def bad_collection():
        raise Exception("Collection not found")
    monkeypatch.setattr(retriever, "_get_collection", bad_collection)
    case = PriorAuthCase(
        case_id="X", payer_id="PAY001", icd10_code="I10", icd10_prefix="I",
        procedure_code="99213", urgency="ROUTINE", age_band="31-55",
        diagnosis_category="Cardiovascular", procedure_type="Office visit", payer_tier=1,
    )
    with pytest.raises(RetrievalError):
        retriever.retrieve(case)

@pytest.mark.implementation
def test_top_k_respected(tier1_cardio_case):
    from case_summary_assistant.retriever import retrieve
    chunks = retrieve(tier1_cardio_case, top_k=3)
    assert len(chunks) <= 3
