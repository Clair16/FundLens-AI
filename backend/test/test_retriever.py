import numpy as np

from app.services.rag.vector_store import (
    create_vector_store
)

from app.services.rag.retriever import (
    retrieve_relevant_chunks
)


def test_retrieve_relevant_chunks():

    chunks = [
        {
            "page_number": 10,
            "text": "The investment objective of the fund."
        },
        {
            "page_number": 23,
            "text": "An exit load of 1 percent may apply."
        },
        {
            "page_number": 31,
            "text": "The expense ratio is charged to the fund."
        }
    ]

    embeddings = np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0]
        ],
        dtype="float32"
    )

    index = create_vector_store(
        embeddings
    )

    results = retrieve_relevant_chunks(
        query="exit load",
        index=index,
        chunks=chunks,
        top_k=2
    )

    assert len(results) == 2

    assert "page_number" in results[0]

    assert "text" in results[0]