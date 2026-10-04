from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app import config


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    """Loaded once on first use, not at import time."""
    return SentenceTransformer(config.EMBEDDING_MODEL)


def create_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]
    return _model().encode(texts, convert_to_numpy=True)


def create_query_embeddings(query):
    return _model().encode([query], convert_to_numpy=True)
