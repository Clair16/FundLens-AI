"""Central settings. Every value comes from the project-root .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = BACKEND_DIR.parent
load_dotenv(ROOT_DIR / ".env", override=True)


def _get(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value and value.strip() else default


GEMINI_API_KEY = _get("GEMINI_API_KEY", "")
GEMINI_MODEL = _get("GEMINI_MODEL", "gemini-2.5-flash")
TEMPERATURE = float(_get("TEMPERATURE", "0.1"))

DATABASE_URL = _get("DATABASE_URL", "sqlite:///./fundlens.db")
EMBEDDING_MODEL = _get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

CHUNK_SIZE = int(_get("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(_get("CHUNK_OVERLAP", "200"))
TOP_K = int(_get("TOP_K", "3"))

MAX_UPLOAD_BYTES = int(_get("MAX_UPLOAD_MB", "25")) * 1024 * 1024
UPLOAD_DIR = BACKEND_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def require_api_key() -> str:
    if not GEMINI_API_KEY or GEMINI_API_KEY.startswith("paste_your"):
        raise RuntimeError("GEMINI_API_KEY is missing. Paste your key into the .env file.")
    return GEMINI_API_KEY
