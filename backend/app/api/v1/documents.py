import json
import re
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import config
from app.database import operations as ops
from app.database.connection import get_db
from app.services.pdf_processing.extractor import extract_text_from_pdf
from app.services.rag.pipeline import analyze_document_with_rag

router = APIRouter(prefix="/documents", tags=["Documents"])


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", Path(name).name)


def _get_or_404(db: Session, document_id: int):
    document = ops.get_document(db, document_id)
    if not document:
        raise HTTPException(404, "Document not found")
    return document


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    content = await file.read()
    if len(content) > config.MAX_UPLOAD_BYTES:
        raise HTTPException(413, f"File exceeds {config.MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit")

    file_path = config.UPLOAD_DIR / f"{uuid.uuid4().hex[:8]}_{_safe_name(file.filename)}"
    file_path.write_bytes(content)

    try:
        pages = extract_text_from_pdf(file_path)
    except Exception:
        file_path.unlink(missing_ok=True)
        raise HTTPException(400, "Could not read this PDF. It may be corrupted or encrypted.")

    document = ops.create_document(db, filename=file.filename, file_path=str(file_path))
    ops.create_pages(db, document.id, pages)

    return {
        "document_id": document.id,
        "filename": document.filename,
        "total_pages": len(pages),
        "status": document.status,
    }


@router.get("")
def list_documents(db: Session = Depends(get_db)):
    return [
        {
            "document_id": d.id,
            "filename": d.filename,
            "status": d.status,
            "overall_risk": d.analysis.overall_risk if d.analysis else None,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in ops.list_documents(db)
    ]


@router.post("/{document_id}/analyze")
def analyze_document(document_id: int, db: Session = Depends(get_db)):
    document = _get_or_404(db, document_id)

    pages = ops.get_page_data(db, document_id)
    if not pages:
        raise HTTPException(404, "Document pages not found")

    try:
        result = analyze_document_with_rag(pages)
    except ValueError as error:      # nothing extractable
        raise HTTPException(422, str(error))
    except RuntimeError as error:    # missing API key
        raise HTTPException(500, str(error))
    except Exception as error:       # LLM / network failure
        raise HTTPException(502, f"Analysis failed: {error}")

    ops.save_analysis(db, document, result.overall_risk, result.model_dump_json())
    return {"document_id": document_id, "filename": document.filename, **result.model_dump()}


@router.get("/{document_id}/analysis")
def get_analysis(document_id: int, db: Session = Depends(get_db)):
    document = _get_or_404(db, document_id)
    if not document.analysis:
        raise HTTPException(404, "This document has not been analyzed yet")
    return {
        "document_id": document_id,
        "filename": document.filename,
        **json.loads(document.analysis.result_json),
    }
