# OPERATIONAL_HANDOFF.md — Mini Project 3

## System summary
Service: Case-Summary Drafting Assistant
Mini Project date: _______________
Approved AI endpoint/deployment: __________________________
Vector store: ChromaDB  Embedding: [approved enterprise embedding service]

## What the service does
Retrieves insurance policy document sections relevant to a prior-auth case,
drafts a structured case summary grounded in retrieved content, quality-checks
it for citation grounding, and stages a handoff package for the care manager.

## What the service does NOT do
- Send any message, email, or notification
- Make a coverage or clinical decision
- Contact any external system

## Status definitions
HANDOFF_READY — Package is staged. Care manager must review and act.
NEEDS_REVIEW  — Low-confidence draft. Care manager must resolve flagged gaps.
PIPELINE_ERROR — Sub-agent failed. No package produced.

## Confidence threshold: 0.70
Below 0.70 → NEEDS_REVIEW regardless of other signals.

## Policy documents in vector store (10 documents)
[List the 10 policy filenames and describe what each covers]

## Two changes required before real pilot
1. _______________
2. _______________

## Known limitations
- Uses synthetic policy documents — real policy documents required for production
- LLM grounding is not perfect — reviewer catches most unverified citations
- No real-time policy document updates — re-ingest required when policies change
