from app import config
from app.services.rag.analyzer import analyze_retrieved_chunks
from app.services.rag.chunker import chunk_pages
from app.services.rag.embeddings import create_embeddings
from app.services.rag.retriever import retrieve_relevant_chunks
from app.services.rag.schemas import AnalysisResult
from app.services.rag.vector_store import create_vector_store

# One retrieval query per thing FundLens reports on.
QUERIES = [
    "What are the important investment risks?",
    "What fees and charges apply, such as expense ratio and exit load?",
    "What lock-in periods or restrictions apply?",
    "What important clauses should an investor review?",
]


def analyze_document_with_rag(pages: list[dict]) -> AnalysisResult:
    """chunk -> embed -> FAISS -> retrieve per topic -> de-duplicate -> Gemini."""
    chunks = chunk_pages(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    if not chunks:
        raise ValueError("No text could be extracted from the document (it may be a scanned PDF).")

    index = create_vector_store(create_embeddings(chunks))

    unique = {}
    for query in QUERIES:
        for chunk in retrieve_relevant_chunks(query, index, chunks, top_k=config.TOP_K):
            unique[(chunk["page_number"], chunk["text"])] = chunk

    ordered = sorted(unique.values(), key=lambda c: c["page_number"])
    return analyze_retrieved_chunks(ordered)
