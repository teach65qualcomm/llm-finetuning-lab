# Project Rules

## Module boundaries
- retriever.py: ChromaDB query only. No LLM calls, no DB writes, no business logic.
- drafter.py: LLM call only. Receives chunks from retriever. Never queries ChromaDB directly.
- reviewer.py: Citation verification only. No LLM calls. Pure Python logic.
- supervisor.py: Orchestration only. Calls retriever, drafter, reviewer in sequence. No rule logic.
- repository.py: All DB reads and writes. No business logic.
- service.py: Idempotency check and coordination only. Do not move pipeline logic here.
- api.py: FastAPI transport only. Do not move business logic here.

## Never do
- Have any agent send a message, email, or notification
- Have the drafter invent policy content not in the retrieved chunks
- Call ChromaDB from drafter.py or reviewer.py
- Load the LLM model inside a per-request function (load once at startup)
- Commit a case without its audit chain
