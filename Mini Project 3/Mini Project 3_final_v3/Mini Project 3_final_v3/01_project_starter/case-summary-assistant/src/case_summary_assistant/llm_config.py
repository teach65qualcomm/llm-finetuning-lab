"""
Approved enterprise AI endpoint configuration and prompt templates.

Task 6: Implement get_llm_client() — configure the approved AI endpoint from environment variables.

This is a configuration-only task. Do not add business logic here.
See: specs/003_drafting_contract.md
"""
from __future__ import annotations
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent / ".env")
except ImportError:
    pass

ENTERPRISE_LLM_ENDPOINT = os.getenv("ENTERPRISE_LLM_ENDPOINT", "")
ENTERPRISE_LLM_API_KEY = os.getenv("ENTERPRISE_LLM_API_KEY", "")
ENTERPRISE_LLM_DEPLOYMENT = os.getenv("ENTERPRISE_LLM_DEPLOYMENT", "")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
TOP_K_CHUNKS = int(os.getenv("TOP_K_CHUNKS", "5"))
CHROMA_PATH = os.getenv("CHROMA_PATH", "vector_store")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "policy_docs")
DATABASE_URL = os.getenv("DATABASE_URL", "data/cases.db")

DRAFTING_PROMPT_TEMPLATE = """
You are a healthcare case summary assistant. Your task is to draft a structured case summary
for a care manager based ONLY on the retrieved policy document sections provided below.

PRIOR-AUTH CASE CONTEXT (anonymized):
{case_context}

RETRIEVED POLICY DOCUMENT SECTIONS:
{chunks}

INSTRUCTIONS:
1. Draft a case summary using ONLY the policy content provided above.
2. Do NOT invent policy rules, coverage limits, or clinical guidance not present in the chunks.
3. The patient_context section must NOT include patient name, date of birth, phone, or email.
4. Cite each policy claim with the source document filename and a brief excerpt.
5. Keep recommended_next_steps actionable and specific to the care manager.

Respond ONLY with a valid JSON object matching this exact schema:
{{
  "patient_context": {{
    "age_band": "...",
    "diagnosis_category": "...",
    "procedure_type": "...",
    "urgency_level": "...",
    "payer_tier": 1
  }},
  "approved_treatment": "...",
  "cited_policy_sections": [
    {{"source_doc": "filename.txt", "excerpt": "exact quote from chunk", "relevance": "why this applies"}}
  ],
  "coverage_notes": "...",
  "recommended_next_steps": ["step 1", "step 2"]
}}
"""


def get_llm_client():
    """
    Return a client configured for the approved enterprise AI endpoint.

    Returns
    -------
    A client instance supplied by the approved enterprise AI integration.

    Raises
    ------
    ValueError
        If required endpoint configuration is missing.
    """
    # ── Mini Project Task 6: Configure the approved enterprise AI endpoint ─────
    if not ENTERPRISE_LLM_ENDPOINT or not ENTERPRISE_LLM_API_KEY or not ENTERPRISE_LLM_DEPLOYMENT:
        raise ValueError(
            "Missing enterprise AI endpoint configuration. Set ENTERPRISE_LLM_ENDPOINT, "
            "ENTERPRISE_LLM_API_KEY, and ENTERPRISE_LLM_DEPLOYMENT in .env."
        )

    from openai import OpenAI

    return OpenAI(base_url=ENTERPRISE_LLM_ENDPOINT, api_key=ENTERPRISE_LLM_API_KEY)
