import numpy as np


def create_vector_store(embeddings):
    import faiss

    embeddings = np.asarray(embeddings, dtype="float32")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index


def search_vector_store(index, query_embedding, top_k=3):
    query_embedding = np.asarray(query_embedding, dtype="float32")
    return index.search(query_embedding, top_k)
