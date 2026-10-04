import json
import re
import uuid
from pathlib import Path
<<<<<<< HEAD
=======

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import config
from app.database import operations as ops
from app.database.connection import get_db
from app.services.pdf_processing.extractor import extract_text_from_pdf
from app.services.rag.pipeline import analyze_document_with_rag

<<<<<<< HEAD
router = APIRouter(prefix="/documents", tags=["Documents"])
=======
from app.database.operations import (
    create_document,
    create_pages,
    create_analysis,
    get_analysis,
    get_all_documents,
    get_all_findings,
    get_dashboard_stats
)
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed

from app.services.rag.chunker import (
    chunk_pages
)

from app.services.rag.pipeline import (
    analyze_document_with_rag
)


# ============================================================
# ROUTER
# ============================================================

def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", Path(name).name)


<<<<<<< HEAD
def _get_or_404(db: Session, document_id: int):
    document = ops.get_document(db, document_id)
    if not document:
        raise HTTPException(404, "Document not found")
    return document
=======
# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed


# ============================================================
# UPLOAD DOCUMENT
# ============================================================

@router.post("/upload")
<<<<<<< HEAD
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
=======
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # SAVE FILE
    # --------------------------------------------------------

    file_path = (
        UPLOAD_DIR /
        file.filename
    )
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed

    content = await file.read()
    if len(content) > config.MAX_UPLOAD_BYTES:
        raise HTTPException(413, f"File exceeds {config.MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit")

<<<<<<< HEAD
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

=======
    with open(
        file_path,
        "wb"
    ) as f:

        f.write(content)


    # --------------------------------------------------------
    # EXTRACT PDF TEXT
    # --------------------------------------------------------

    pages = extract_text_from_pdf(
        file_path
    )


    # --------------------------------------------------------
    # CREATE DOCUMENT
    # --------------------------------------------------------

    document = create_document(
        db=db,
        filename=file.filename,
        file_path=str(file_path)
    )


    # --------------------------------------------------------
    # SAVE PAGES
    # --------------------------------------------------------

    create_pages(
        db=db,
        document_id=document.id,
        pages=pages
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "message":
            "Document processed successfully",

        "document_id":
            document.id,

        "filename":
            document.filename,

        "total_pages":
            len(pages),

        "status":
            document.status
    }


# ============================================================
# CREATE CHUNKS
# ============================================================

@router.post("/{document_id}/chunks")
def create_document_chunks(
    document_id: int,
    db: Session = Depends(get_db)
):

    from app.database.models import Page


    # --------------------------------------------------------
    # GET PAGES
    # --------------------------------------------------------

    pages = (
        db.query(Page)
        .filter(
            Page.document_id ==
            document_id
        )
        .order_by(
            Page.page_number
        )
        .all()
    )


    if not pages:

        return {
            "error":
                "Document pages not found"
        }


    # --------------------------------------------------------
    # PAGE DATA
    # --------------------------------------------------------

    page_data = [

        {
            "page_number":
                page.page_number,

            "text":
                page.text
        }

        for page in pages

    ]


    # --------------------------------------------------------
    # CREATE CHUNKS
    # --------------------------------------------------------

    chunks = chunk_pages(
        page_data
    )


    return {

        "document_id":
            document_id,

        "total_chunks":
            len(chunks),

        "chunks":
            chunks
    }
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed


# ============================================================
# ANALYZE DOCUMENT
# ============================================================

@router.post("/{document_id}/analyze")
<<<<<<< HEAD
def analyze_document(document_id: int, db: Session = Depends(get_db)):
    document = _get_or_404(db, document_id)

    pages = ops.get_page_data(db, document_id)
=======
def analyze_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    from app.database.models import Page


    # --------------------------------------------------------
    # GET DOCUMENT PAGES
    # --------------------------------------------------------

    pages = (
        db.query(Page)
        .filter(
            Page.document_id ==
            document_id
        )
        .order_by(
            Page.page_number
        )
        .all()
    )


>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed
    if not pages:
        raise HTTPException(404, "Document pages not found")

<<<<<<< HEAD
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
=======
        return {

            "error":
                "Document pages not found"
        }


    # --------------------------------------------------------
    # PAGE DATA
    # --------------------------------------------------------

    page_data = [

        {
            "page_number":
                page.page_number,

            "text":
                page.text
        }

        for page in pages

    ]


    # --------------------------------------------------------
    # RUN RAG PIPELINE
    # --------------------------------------------------------

    analysis = analyze_document_with_rag(
        page_data
    )


    # --------------------------------------------------------
    # SAVE ANALYSIS TO DATABASE
    # --------------------------------------------------------

    saved_analysis = create_analysis(

        db=db,

        document_id=document_id,

        analysis_data=analysis
    )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "message":
            "Document analyzed successfully",

        "document_id":
            document_id,

        "analysis_id":
            saved_analysis.id,

        "analysis":
            analysis.model_dump()
    }


# ============================================================
# GET DOCUMENT ANALYSIS
# ============================================================

@router.get("/{document_id}/analysis")
def get_document_analysis(
    document_id: int,
    db: Session = Depends(get_db)
):

    analysis = get_analysis(

        db=db,

        document_id=document_id
    )


    if not analysis:

        return {

            "error":
                "Analysis not found"
        }


    return {

        "document_id":
            document_id,

        "analysis_id":
            analysis.id,

        "overall_risk":
            analysis.overall_risk,

        "summary":
            analysis.summary,

        "findings": [

            {

                "category":
                    finding.category,

                "title":
                    finding.title,

                "severity":
                    finding.severity,

                "explanation":
                    finding.explanation,

                "page_number":
                    finding.page_number,

                "evidence":
                    finding.evidence
            }

            for finding in analysis.findings

        ]
    }


# ============================================================
# DASHBOARD STATS
# ============================================================

@router.get("/dashboard/stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):

    return get_dashboard_stats(
        db
    )


# ============================================================
# DASHBOARD FINDINGS
# ============================================================

@router.get("/dashboard/findings")
def dashboard_findings(
    db: Session = Depends(get_db)
):

    findings = get_all_findings(
        db
    )


    return {

        "findings": [

            {

                "id":
                    finding.id,

                "analysis_id":
                    finding.analysis_id,

                "category":
                    finding.category,

                "title":
                    finding.title,

                "severity":
                    finding.severity,

                "explanation":
                    finding.explanation,

                "page_number":
                    finding.page_number,

                "evidence":
                    finding.evidence
            }

            for finding in findings

        ]
    }


# ============================================================
# DASHBOARD DOCUMENTS
# ============================================================

@router.get("/dashboard/documents")
def dashboard_documents(
    db: Session = Depends(get_db)
):

    documents = get_all_documents(
        db
    )


    return {

        "documents": [

            {

                "id":
                    document.id,

                "filename":
                    document.filename,

                "status":
                    document.status,

                "created_at":
                    (
                        document.created_at.isoformat()
                        if document.created_at
                        else None
                    )
            }

            for document in documents

        ]
    }
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed
