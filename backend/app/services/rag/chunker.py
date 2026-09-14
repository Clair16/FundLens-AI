def chunk_pages(
        pages,
        chunk_size = 1000,
        chunk_overlap = 200
):
    chunks = []
    for page in pages:
        text = page['text']
        page_number = page['page_number']

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    'page_number':page_number,
                    'text': chunk_text
                }
                )
            start += chunk_size -chunk_overlap
    return chunks
