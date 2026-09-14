from app.services.rag.embeddings import (create_query_embeddings)

from app.services.rag.vector_store import (search_vector_store)

def retrieve_relevent_chunks(
        query,
        index,
        chunks,
        top_k = 3
):
    query_embedding = create_query_embeddings(query)
    distances, indices = search_vector_store(
        index,
        query_embedding,
        top_k=top_k
    )

    results = []

    for distance, index_position in zip(
        distances[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        chunk = chunks[index_position]

        results.append(
            {
                "page_number": chunk["page_number"],
                "text": chunk["text"],
                "distance": float(distance)
            }
        )

    return results