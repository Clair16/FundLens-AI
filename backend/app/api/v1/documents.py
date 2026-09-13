from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from app.services.pdf_processing.extractor import (
    extract_text_from_pdf
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # -----------------------------
    # Save uploaded file
    # -----------------------------

    file_path = UPLOAD_DIR / file.filename

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # -----------------------------
    # Extract PDF text
    # -----------------------------

    pages = extract_text_from_pdf(
        file_path
    )

    # -----------------------------
    # Response
    # -----------------------------

    return {
        "message": "Document processed successfully",
        "filename": file.filename,
        "size": len(content),
        "total_pages": len(pages),
        "pages": pages
    }