from sqlalchemy.orm import Session

from app.database.models import Analysis, Document, Page


def create_document(db: Session, filename: str, file_path: str) -> Document:
    document = Document(filename=filename, file_path=file_path, status="uploaded")
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def create_pages(db: Session, document_id: int, pages: list[dict]) -> None:
    db.add_all(
        Page(document_id=document_id, page_number=p["page_number"], text=p["text"])
        for p in pages
    )
    db.commit()


def get_document(db: Session, document_id: int) -> Document | None:
    return db.get(Document, document_id)


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
