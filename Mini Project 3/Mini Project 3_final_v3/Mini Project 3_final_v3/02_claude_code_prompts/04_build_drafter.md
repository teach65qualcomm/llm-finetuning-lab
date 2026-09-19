# Prompt 4 — Build the Drafting Agent (Tasks 2 & 6)
First complete Task 6: implement get_llm_client() in llm_config.py.
Then complete Task 2: implement draft() in drafter.py.

Rules:
- Use ONLY chunk text passed in — never invent policy content
- patient_context must exclude name, DOB, phone, email
- Parse LLM JSON response into CaseSummary object
- Raise DraftingError if parsing fails

Run: `python -m pytest tests/test_drafter.py -q`
Use mock LLM responses in tests — do not call real LLM in tests.
