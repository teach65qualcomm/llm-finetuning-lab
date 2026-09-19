# Prompt 1 — Scout the Repository
Explore without making changes. Read CLAUDE.md, .claude/rules/, specs/, domain.py, policies/ (at least 3 files), tests/.

Provide:
1. What this service does and must never do
2. The four-agent architecture and responsibility of each agent
3. The 6 implementation tasks and which file each is in
4. The RAG pipeline: how ChromaDB is queried, what chunks contain
5. The safety boundary: HANDOFF_READY vs NEEDS_REVIEW vs PIPELINE_ERROR
6. The confidence threshold and what triggers FLAG_FOR_HUMAN

Do NOT propose external APIs, new agents, or changes to tests.
Every statement must cite a file in this repository.
