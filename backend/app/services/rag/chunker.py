from app import config


def chunk_pages(pages, chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP):
    """Split each page into overlapping character chunks, keeping the page number."""
    step = chunk_size - chunk_overlap
    if step <= 0:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    for page in pages:
        text = page["text"]
        for start in range(0, len(text), step):
            piece = text[start:start + chunk_size].strip()
            if piece:
                chunks.append({"page_number": page["page_number"], "text": piece})
    return chunks
