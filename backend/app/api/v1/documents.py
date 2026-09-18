from pathlib import Path

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
    create_pages,
    create_analysis,
    get_analysis,
    get_all_documents,
    get_all_findings,
    get_dashboard_stats
)

from app.services.rag.chunker import (
    chunk_pages
)

from app.services.rag.pipeline import (
    analyze_document_with_rag
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = Path("data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# UPLOAD DOCUMENT
# ============================================================

@router.post("/upload")
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

    content = await file.read()

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


# ============================================================
# ANALYZE DOCUMENT
# ============================================================

@router.post("/{document_id}/analyze")
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