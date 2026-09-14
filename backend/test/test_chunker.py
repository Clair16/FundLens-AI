from app.services.rag.chunker import chunk_pages


def test_chunk_pages():

    pages = [
        {
            "page_number": 1,
            "text": "A" * 2500
        }
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=1000,
        chunk_overlap=200
    )

    assert len(chunks) > 1

    assert chunks[0]["page_number"] == 1

    assert len(chunks[0]["text"]) <= 1000