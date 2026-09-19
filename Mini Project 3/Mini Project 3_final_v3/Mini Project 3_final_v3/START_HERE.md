# Mini Project 3 — Start Here
## Case-Summary Drafting Assistant

**Prerequisite:** Mini Project 2 complete.

## Setup (4 commands)
```bash
cd 01_project_starter/case-summary-assistant
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/ingest_policies.py        # load policy docs into ChromaDB
```

## Verify baseline
```bash
python -m pytest -m baseline -q
# Expected: 12 passed, 36 deselected
```

## Then read
Open `Mini Project_3_Learner_Implementation_Guide.pdf` and keep it open throughout.
