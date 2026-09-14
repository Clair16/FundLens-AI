from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.connection import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    status = Column(
        String(50),
        default="uploaded"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    pages = relationship(
        "Page",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class Page(Base):

    __tablename__ = "pages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )

    page_number = Column(
        Integer,
        nullable=False
    )

    text = Column(
        Text,
        nullable=False
    )

    document = relationship(
        "Document",
        back_populates="pages"
    )