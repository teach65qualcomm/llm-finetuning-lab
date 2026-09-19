# Evaluation Rubric — Mini Project 3

| Section | Points | Key criteria |
|---------|--------|-------------|
| RAG retrieval agent (Task 1) | 15 | Correct chunks returned, sorted, RetrievedChunk objects, RetrievalError on empty |
| Drafting agent (Task 2) | 15 | CaseSummary grounded in chunks, anonymized patient context, DraftingError on parse failure |
| Review agent (Task 3) | 15 | Correct confidence scoring, FLAG_FOR_HUMAN below 0.70, flagged gaps populated |
| Supervisor (Task 4) | 20 | Stage order, correct status mapping, 4 events on success, 1 on failure |
| Persistence & audit (Task 5) | 15 | Atomic transaction, idempotency, append-only, no PII in audit |
| API verification | 10 | All endpoints correct, 422 on forbidden fields, dashboard shows cited docs |
| Test coverage | 5 | >= 80% |
| Submission quality | 5 | TEST_RESULTS.md and OPERATIONAL_HANDOFF.md with observed evidence |
| **Total** | **100** | Minimum passing: 70/100 |

## Automatic fail conditions
- Service sends any message or contacts any external party
- Summary contains patient name, DOB, or contact details
- Drafter invents policy content not in retrieved chunks
- TEST_RESULTS.md contains planned rather than observed values
