from sqlalchemy.orm import Session

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

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


# ============================================================
# PAGE OPERATIONS
# ============================================================

def create_pages(
    db: Session,
    document_id: int,
    pages: list
):
    for page in pages:

        db_page = Page(
            document_id=document_id,
            page_number=page["page_number"],
            text=page["text"]
        )

        db.add(db_page)

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