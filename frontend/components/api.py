import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
API = f"{BACKEND_URL}/api/v1/documents"


def _json(response):
    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(detail)
    return response.json()


def upload_pdf(file):
    response = requests.post(
        f"{API}/upload",
        files={"file": (file.name, file.getvalue(), "application/pdf")},
        timeout=120,
    )
    return _json(response)


def analyze(document_id):
    return _json(requests.post(f"{API}/{document_id}/analyze", timeout=300))


def get_analysis(document_id):
    return _json(requests.get(f"{API}/{document_id}/analysis", timeout=30))


def list_documents():
    return _json(requests.get(API, timeout=30))
