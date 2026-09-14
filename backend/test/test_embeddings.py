from app.services.rag.embeddings import create_embeddings

def test_create_embeddings():
    chunks = [
        {
            'page_number':1,
            'text': 'this is a mutual fund document.'
        },
        {
            "page_number": 2,
            "text": "An exit load may apply."
        }
    ]

    embeddings = create_embeddings(chunks)

    assert len(embeddings) == 2
    assert embeddings.shape[1] > 0