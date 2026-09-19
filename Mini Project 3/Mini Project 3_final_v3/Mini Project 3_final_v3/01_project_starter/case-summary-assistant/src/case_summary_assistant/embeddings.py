"""
Approved enterprise embedding function, shared by ingestion and retrieval so
that both sides of the vector store use the same embedding space.

No live enterprise embedding endpoint is reachable in this training
environment, so this is a deterministic, dependency-free hashing-trick
vectorizer (pure Python + numpy — no network call, no model download, no
ChromaDB DefaultEmbeddingFunction). Swap this class for your organisation's
real embedding endpoint/SDK call before shipping; nothing else needs to
change since both ingest_policies.py and retriever.py import it from here.
"""
from __future__ import annotations
import hashlib
import re

import numpy as np
from chromadb import Documents, EmbeddingFunction, Embeddings

EMBEDDING_DIM = 384


class CompanyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            vec = np.zeros(EMBEDDING_DIM, dtype=np.float64)
            tokens = re.findall(r"[a-z0-9]+", text.lower())
            for token in tokens:
                digest = hashlib.sha256(token.encode()).digest()
                idx = int.from_bytes(digest[:4], "little") % EMBEDDING_DIM
                sign = 1.0 if digest[4] % 2 == 0 else -1.0
                vec[idx] += sign  # random-sign hashing trick reduces collision bias
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            embeddings.append(vec.tolist())
        return embeddings
