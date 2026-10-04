# FundLens AI

RAG-based, AI-powered mutual fund document risk analyzer and simplifier.
Upload a mutual fund PDF and FundLens extracts the **risks, fees, restrictions and key clauses**,
each rated Low / Medium / High, explained in plain language, with the **page number and an
evidence quote** from the document.

## How it works

```
PDF -> PyMuPDF (text per page) -> SQLite/PostgreSQL
    -> chunk (1000 chars, 200 overlap) -> MiniLM embeddings -> FAISS
    -> retrieve top chunks for 4 topics (risks, fees, restrictions, clauses)
    -> Gemini (structured JSON) -> stored in DB -> Streamlit UI
```

## Setup

```bash
pip install -r requirements.txt
```

Open the **`.env`** file in the project root and paste your Gemini API key into
`GEMINI_API_KEY`. That is the only edit needed; every other setting has a default.

## Run

Terminal 1 (backend):
```bash
cd backend
uvicorn app.main:app --reload
```

Terminal 2 (frontend):
```bash
cd frontend
streamlit run app.py
```

API docs: http://127.0.0.1:8000/docs

## API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/documents/upload` | Upload a PDF, extract and store pages |
| GET  | `/api/v1/documents` | List documents and their overall risk |
| POST | `/api/v1/documents/{id}/analyze` | Run the RAG analysis and save it |
| GET  | `/api/v1/documents/{id}/analysis` | Fetch a saved analysis |

## Tests

```bash
cd backend
pytest
```

## Structure

```
.env                         all configuration
requirements.txt
backend/app/
  config.py                  reads .env
  main.py                    FastAPI app
  api/v1/documents.py        routes
  database/                  connection, models (Document, Page, Analysis), operations
  services/pdf_processing/   extractor.py
  services/rag/              chunker, embeddings, vector_store, retriever, analyzer, pipeline, schemas
backend/test/                unit tests
frontend/
  app.py                     Streamlit entry
  components/                api, upload, header, dashboard, risk_card
```

> FundLens AI explains what a document says. It is not investment advice.
