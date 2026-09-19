"""
Ingest synthetic policy documents into ChromaDB vector store.
Run once before starting implementation: python scripts/ingest_policies.py
"""
import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from case_summary_assistant.llm_config import CHROMA_PATH, CHROMA_COLLECTION

POLICIES_DIR = Path(__file__).parent.parent / "policies"
CHUNK_SIZE = 400       # characters
CHUNK_OVERLAP = 80     # characters


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end].strip())
        start += size - overlap
    return [c for c in chunks if len(c) > 50]


def ingest():
    import chromadb

    # IMPORTANT — Embedding policy:
    # Use only the embedding endpoint or SDK approved by your organisation.
    # Do NOT use DefaultEmbeddingFunction from ChromaDB.
    # Ask your trainer/admin for the approved embedding endpoint or SDK.
    #
    # The approved-endpoint stand-in used here lives in
    # case_summary_assistant/embeddings.py so retriever.py can open the
    # collection with the exact same embedding function used at ingest time.
    from case_summary_assistant.embeddings import CompanyEmbeddingFunction

    print(f"Using ChromaDB at: {CHROMA_PATH}")
    print(f"Collection: {CHROMA_COLLECTION}")

    ef = CompanyEmbeddingFunction()
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Delete and recreate for clean ingest
    try:
        client.delete_collection(CHROMA_COLLECTION)
        print("Cleared existing collection.")
    except Exception:
        pass

    collection = client.create_collection(name=CHROMA_COLLECTION, embedding_function=ef)

    policy_files = sorted(POLICIES_DIR.glob("*.txt"))
    if not policy_files:
        print(f"ERROR: No .txt files found in {POLICIES_DIR}")
        sys.exit(1)

    total_chunks = 0
    for policy_file in policy_files:
        text = policy_file.read_text()
        chunks = chunk_text(text)
        ids, docs, metas = [], [], []
        for i, chunk in enumerate(chunks):
            # Extract page number from chunk if mentioned
            page = 1
            for line in chunk.split("\n"):
                if line.strip().startswith("PAGE "):
                    try:
                        page = int(line.strip().split()[1])
                    except (IndexError, ValueError):
                        pass
            ids.append(f"{policy_file.stem}_{i:04d}")
            docs.append(chunk)
            metas.append({"source": policy_file.name, "page": page})

        collection.add(documents=docs, metadatas=metas, ids=ids)
        total_chunks += len(chunks)
        print(f"  ✅ {policy_file.name}: {len(chunks)} chunks")

    print(f"\n✅ Ingestion complete: {len(policy_files)} documents → {total_chunks} chunks")
    print(f"   Vector store: {CHROMA_PATH}/{CHROMA_COLLECTION}")


if __name__ == "__main__":
    ingest()
