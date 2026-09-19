# TEST_RESULTS.md — Mini Project 3

Learner name: _______________
Submission date: _______________

## Automated test results
Paste output of: `python -m pytest --cov=case_summary_assistant --cov-report=term-missing --cov-fail-under=80`
```
[PASTE OUTPUT HERE]
```

## Manual sample case results
| Sample | Expected status | Actual status | Confidence | Pass/Fail |
|--------|----------------|---------------|-----------|-----------|
| high_confidence_tier1_cardiovascular | HANDOFF_READY | | | |
| medium_confidence_tier2_musculoskeletal | HANDOFF_READY or NEEDS_REVIEW | | | |
| low_confidence_tier3_oncology | NEEDS_REVIEW | | | |
| idempotency_test (2nd call) | idempotent_replay: true | | N/A | |

## Idempotency verification
- First call case_id: _______________
- Second call idempotent_replay: _______________ (must be true)
- Database case count after 2 calls: _______________ (must be 1)

## Audit safety verification
Confirm none of these appear in agent_audit_events:
- [ ] Patient name
- [ ] Date of birth
- [ ] Full summary text
- [ ] Full chunk text
