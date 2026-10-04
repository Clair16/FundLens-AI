import fitz  # PyMuPDF


def extract_text_from_pdf(file_path) -> list[dict]:
    """Return [{'page_number': int, 'text': str}, ...] for every page."""
    with fitz.open(file_path) as document:
        return [
            {"page_number": number, "text": page.get_text().strip()}
            for number, page in enumerate(document, start=1)
        ]
