# 001 — Project Scope

## What this service does
Retrieves relevant insurance policy document sections, drafts a structured case summary
grounded in retrieved content, quality-checks it for citation grounding, and stages a
handoff package for the care manager.

## What this service does NOT do
- Send any message, email, or notification to any party
- Make a coverage, clinical, or payment decision
- Contact any external system (insurer, EMR, patient portal)
- Replace the care manager

## Status definitions
HANDOFF_READY  — Package staged, care manager must review and act
NEEDS_REVIEW   — Low-confidence draft, care manager must actively resolve flagged gaps
PIPELINE_ERROR — A sub-agent failed; no package produced
