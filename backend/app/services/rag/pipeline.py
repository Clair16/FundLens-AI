from app.services.rag.chunker import (
    chunk_pages
)

from app.services.rag.embeddings import (
    create_embeddings
)

from app.services.rag.vector_store import (
    create_vector_store
)

from app.services.rag.retriever import (
    retrieve_relevant_chunks
)

from app.services.rag.analyzer import (
    analyze_retrieved_chunks
)


def analyze_document_with_rag(
    pages
):

    # --------------------------------
    # 1. Create chunks
    # --------------------------------

    chunks = chunk_pages(
        pages,
        chunk_size=1000,
        chunk_overlap=200
    )

    if not chunks:
        raise ValueError(
            "No text could be extracted "
            "from the document."
        )

    # --------------------------------
    # 2. Create embeddings
    # --------------------------------

    embeddings = create_embeddings(
        chunks
    )

    # --------------------------------
    # 3. Create FAISS index
    # --------------------------------

    index = create_vector_store(
        embeddings
    )

    # --------------------------------
    # 4. Retrieve for multiple topics
    # --------------------------------

    queries = [
        "What are the important investment risks?",
        "What fees and charges apply?",
        "What lock-in periods or restrictions apply?",
        "What important clauses should an investor review?"
    ]

    retrieved_chunks = []

    for query in queries:

        results = retrieve_relevant_chunks(
            query=query,
            index=index,
            chunks=chunks,
            top_k=3
        )

        retrieved_chunks.extend(
            results
        )

    # --------------------------------
    # 5. Remove duplicate chunks
    # --------------------------------

    unique_chunks = {}

    for chunk in retrieved_chunks:

        key = (
            chunk["page_number"],
            chunk["text"]
        )

        unique_chunks[key] = chunk

    retrieved_chunks = list(
        unique_chunks.values()
    )

    # --------------------------------
    # 6. Send retrieved context to Gemini
    # --------------------------------

    analysis = analyze_retrieved_chunks(
        retrieved_chunks
    )

    return analysis