from pathlib import Path
from app.services.rag.chunker import chunk_pages

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from app.services.pdf_processing.extractor import (
    extract_text_from_pdf
)

from app.database.connection import get_db

from app.database.operations import (
    create_document,
    create_pages
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
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # -----------------------------
    # Save PDF
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
    # Save document to database
    # -----------------------------

    document = create_document(
        db=db,
        filename=file.filename,
        file_path=str(file_path)
    )

    # -----------------------------
    # Save pages to database
    # -----------------------------

    create_pages(
        db=db,
        document_id=document.id,
        pages=pages
    )

    # -----------------------------
    # Response
    # -----------------------------

    return {
        "message": "Document processed successfully",
        "document_id": document.id,
        "filename": document.filename,
        "total_pages": len(pages),
        "status": document.status
    }

@router.post("/{document_id}/chunks")
def create_document_chunks(
    document_id: int,
    db: Session = Depends(get_db)
):

    from app.database.models import Page

    pages = (
        db.query(Page)
        .filter(Page.document_id == document_id)
        .order_by(Page.page_number)
        .all()
    )

    page_data = [
        {
            "page_number": page.page_number,
            "text": page.text
        }
        for page in pages
    ]

    chunks = chunk_pages(
        page_data
    )

    return {
        "document_id": document_id,
        "total_chunks": len(chunks),
        "chunks": chunks
    }