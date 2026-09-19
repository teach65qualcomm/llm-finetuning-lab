# Testing Rules

## Test-first behavior
- Run the failing test before writing any implementation code.
- Implement only enough to make that test pass.
- Run the full test file before moving to the next task.

## Do not edit tests
A test change is justified ONLY when the test and an approved specification genuinely disagree.

## Required failure paths
- retriever.py: RetrievalError when vector store is empty
- drafter.py: DraftingError when LLM response cannot be parsed
- reviewer.py: FLAG_FOR_HUMAN when confidence < 0.70
- supervisor.py: PIPELINE_ERROR when any sub-agent raises an exception
- repository.py: idempotent_replay on duplicate case_id
- audit: UPDATE and DELETE on agent_audit_events must fail
