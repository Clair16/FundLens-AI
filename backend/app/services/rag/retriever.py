from app import config
from app.services.rag.embeddings import create_query_embeddings
from app.services.rag.vector_store import search_vector_store


def retrieve_relevant_chunks(query, index, chunks, top_k=config.TOP_K, query_embedding=None):
    """Return the top_k chunks closest to the query.

    If query_embedding is given it is used directly, otherwise the query is embedded.
    """
    if query_embedding is None:
        query_embedding = create_query_embeddings(query)

    distances, indices = search_vector_store(index, query_embedding, top_k=top_k)

    results = []
    for distance, position in zip(distances[0], indices[0]):
        if position == -1:  # fewer chunks than top_k
            continue
        chunk = chunks[position]
        results.append({
            "page_number": chunk["page_number"],
            "text": chunk["text"],
            "distance": float(distance),
        })
    return results
