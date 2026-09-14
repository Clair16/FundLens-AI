import numpy as np

from app.services.rag.vector_store import (
    create_vector_store,
    search_vector_store
)


def test_vector_store():

    embeddings = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ],
        dtype="float32"
    )

    index = create_vector_store(
        embeddings
    )

    assert index.ntotal == 3

    query = np.array(
        [[1.0, 0.0, 0.0]],
        dtype="float32"
    )

    distances, indices = search_vector_store(
        index,
        query,
        top_k=2
    )

    assert indices.shape == (1, 2)

    assert indices[0][0] == 0