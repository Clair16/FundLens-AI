from sqlalchemy.orm import Session

from app.database.models import Document, Page


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