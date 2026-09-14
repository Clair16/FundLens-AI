import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

from app.services.rag.schemas import AnalysisResult


load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


MODEL_NAME = "gemini-2.5-flash"


def analyze_retrieved_chunks(
    retrieved_chunks
):

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"""
[Page {chunk["page_number"]}]

{chunk["text"]}
"""
        )

    context = "\n".join(
        context_parts
    )

    prompt = f"""
You are FundLens AI, a mutual-fund
document analysis assistant.

Analyze ONLY the provided document
context.

Your job is to identify:

1. Important risks
2. Fees and charges
3. Restrictions and lock-in conditions
4. Important clauses investors should review

For every finding:

- Assign Low, Medium, or High severity.
- Explain the finding in simple language.
- Provide the page number.
- Provide a short evidence quote taken
  directly from the supplied context.

IMPORTANT RULES:

- Do not invent information.
- Do not use outside knowledge.
- Do not provide direct investment advice.
- Only report information supported by
  the supplied context.
- The page number must correspond to the
  page label in the supplied context.
- If the context does not contain enough
  information, do not make up a finding.

Document context:

{context}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AnalysisResult
        )
    )

    return AnalysisResult.model_validate_json(
        response.text
    )