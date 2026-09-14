from app.services.rag.chunker import chunk_pages

from app.services.rag.embeddings import create_embeddings

from app.services.rag.vector_store import create_vector_store

from app.services.rag.retriever import retrieve_relevant_chunks


def test_real_semantic_retrieval():

    pages = [
        {
            "page_number": 10,
            "text": (
                "The investment objective of the scheme "
                "is to generate long term capital appreciation."
            )
        },
        {
            "page_number": 23,
            "text": (
                "An exit load of 1 percent will be charged "
                "if units are redeemed within one year."
            )
        },
        {
            "page_number": 31,
            "text": (
                "The expense ratio represents the annual "
                "operating expenses charged to the scheme."
            )
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=500,
        chunk_overlap=50
    )

    embeddings = create_embeddings(
        chunks
    )

    index = create_vector_store(
        embeddings
    )

    results = retrieve_relevant_chunks(
        query="What is the exit load?",
        index=index,
        chunks=chunks,
        top_k=1
    )

    assert len(results) == 1

    assert results[0]["page_number"] == 23

    assert "exit load" in (
        results[0]["text"].lower()
    )