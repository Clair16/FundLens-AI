from sqlalchemy.orm import Session

<<<<<<< HEAD
from app.database.models import Analysis, Document, Page


def create_document(db: Session, filename: str, file_path: str) -> Document:
    document = Document(filename=filename, file_path=file_path, status="uploaded")
=======
from app.database.models import (
    Document,
    Page,
    Analysis,
    RiskFinding
)


# ============================================================
# DOCUMENT OPERATIONS
# ============================================================

def create_document(
    db: Session,
    filename: str,
    file_path: str
):
    document = Document(
        filename=filename,
        file_path=file_path,
        status="processed"
    )

>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


<<<<<<< HEAD
def create_pages(db: Session, document_id: int, pages: list[dict]) -> None:
    db.add_all(
        Page(document_id=document_id, page_number=p["page_number"], text=p["text"])
        for p in pages
    )
    db.commit()

=======
# ============================================================
# PAGE OPERATIONS
# ============================================================

def create_pages(
    db: Session,
    document_id: int,
    pages: list
):
    for page in pages:
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed

def get_document(db: Session, document_id: int) -> Document | None:
    return db.get(Document, document_id)


<<<<<<< HEAD
def get_page_data(db: Session, document_id: int) -> list[dict]:
    pages = (
        db.query(Page)
        .filter(Page.document_id == document_id)
        .order_by(Page.page_number)
        .all()
    )
    return [{"page_number": p.page_number, "text": p.text} for p in pages]


def list_documents(db: Session) -> list[Document]:
    return db.query(Document).order_by(Document.created_at.desc()).all()


def save_analysis(db: Session, document: Document, overall_risk: str, result_json: str) -> Analysis:
    """Insert or replace the analysis for a document."""
    analysis = document.analysis or Analysis(document_id=document.id)
    analysis.overall_risk = overall_risk
    analysis.result_json = result_json
    document.status = "analyzed"
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis
=======
    db.commit()


# ============================================================
# ANALYSIS OPERATIONS
# ============================================================

def create_analysis(
    db: Session,
    document_id: int,
    analysis_data
):
    analysis = Analysis(
        document_id=document_id,
        overall_risk=analysis_data.overall_risk,
        summary=analysis_data.summary
    )

    db.add(analysis)

    # Get analysis ID before inserting findings
    db.flush()

    for finding in analysis_data.findings:

        db_finding = RiskFinding(
            analysis_id=analysis.id,
            category=finding.category,
            title=finding.title,
            severity=finding.severity,
            explanation=finding.explanation,
            page_number=finding.page_number,
            evidence=finding.evidence
        )

        db.add(db_finding)

    db.commit()
    db.refresh(analysis)

    return analysis


def get_analysis(
    db: Session,
    document_id: int
):
    return (
        db.query(Analysis)
        .filter(
            Analysis.document_id == document_id
        )
        .first()
    )


# ============================================================
# DASHBOARD OPERATIONS
# ============================================================

def get_all_documents(db: Session):

    return (
        db.query(Document)
        .order_by(
            Document.created_at.desc()
        )
        .all()
    )


def get_all_findings(db: Session):

    return (
        db.query(RiskFinding)
        .order_by(
            RiskFinding.id.desc()
        )
        .all()
    )


def get_dashboard_stats(db: Session):

    documents = get_all_documents(db)
    findings = get_all_findings(db)

    stats = {
        "documents": len(documents),

        "risks": 0,

        "fees": 0,

        "restrictions": 0,

        "clauses": 0,

        "high": 0,

        "medium": 0,

        "low": 0
    }

    for finding in findings:

        category = finding.category

        severity = finding.severity


        # -------------------------------
        # CATEGORY COUNT
        # -------------------------------

        if category == "Risk":

            stats["risks"] += 1

        elif category == "Fee":

            stats["fees"] += 1

        elif category == "Restriction":

            stats["restrictions"] += 1

        elif category == "Important Clause":

            stats["clauses"] += 1


        # -------------------------------
        # SEVERITY COUNT
        # -------------------------------

        if severity == "High":

            stats["high"] += 1

        elif severity == "Medium":

            stats["medium"] += 1

        elif severity == "Low":

            stats["low"] += 1


    return stats
>>>>>>> 77f8a9c485b6c641decd5873e728fec745e429ed
