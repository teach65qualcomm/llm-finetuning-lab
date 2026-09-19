# 004 — Review Contract

## Input
CaseSummary + list of RetrievedChunk objects (same chunks passed to drafter)

## Citation verification
For each cited_policy_section in the summary:
  - Check if the cited excerpt appears (case-insensitive, stripped) in any retrieved chunk text
  - If yes: verified citation
  - If no: unverified citation → add to flagged_gaps

## Confidence score
confidence_score = verified_citations / total_citations
If total_citations == 0: confidence_score = 1.0

Rationale: a summary with no policy citations has no unverified claims. The absence
of citations is not itself a failure — it results in confidence_score = 1.0 and
recommendation = APPROVE. The drafting agent is separately responsible for including
grounded citations; the reviewer only checks the citations that are present.

## Recommendation
FLAG_FOR_HUMAN if confidence_score < CONFIDENCE_THRESHOLD (default 0.70)
APPROVE if confidence_score >= CONFIDENCE_THRESHOLD

## Output: ReviewResult fields
- confidence_score: float (0.0–1.0)
- flagged_gaps: list[str] — description of each unverified citation
- recommendation: str — "APPROVE" or "FLAG_FOR_HUMAN"

## Constraints
- No LLM calls in the reviewer — pure Python citation matching
- Never modify the summary
