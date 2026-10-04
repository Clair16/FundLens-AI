from functools import lru_cache

from google import genai
from google.genai import types

from app import config
from app.services.rag.schemas import AnalysisResult

PROMPT = """You are FundLens AI, a mutual-fund document analysis assistant.

Analyze ONLY the provided document context and identify:
1. Important risks
2. Fees and charges
3. Restrictions and lock-in conditions
4. Important clauses investors should review

For every finding:
- Assign Low, Medium, or High severity.
- Explain it in simple language a first-time investor can understand.
- Give the page number.
- Give a short evidence quote copied directly from the supplied context.

Also give an overall_risk rating and a 2-3 sentence plain-language summary.

RULES:
- Do not invent information or use outside knowledge.
- Do not give direct investment advice (no buy/sell/hold recommendations).
- Only report information supported by the supplied context.
- The page number must match the page label in the context.
- If the context lacks enough information, do not make up a finding.

Document context:
{context}
"""


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    return genai.Client(api_key=config.require_api_key())


def analyze_retrieved_chunks(retrieved_chunks) -> AnalysisResult:
    context = "\n".join(
        f"\n[Page {c['page_number']}]\n{c['text']}\n" for c in retrieved_chunks
    )

    response = _client().models.generate_content(
        model=config.GEMINI_MODEL,
        contents=PROMPT.format(context=context),
        config=types.GenerateContentConfig(
            temperature=config.TEMPERATURE,
            response_mime_type="application/json",
            response_schema=AnalysisResult,
        ),
    )
    return AnalysisResult.model_validate_json(response.text)
