from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.connection import Base


def _now():
    return datetime.now(timezone.utc)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    status = Column(String(50), default="uploaded")  # uploaded -> analyzed
    created_at = Column(DateTime, default=_now)

    pages = relationship("Page", back_populates="document", cascade="all, delete-orphan")
    analysis = relationship("Analysis", back_populates="document", uselist=False,
                            cascade="all, delete-orphan")


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    document = relationship("Document", back_populates="pages")


class Analysis(Base):
    """Stored RAG result so the dashboard can show past analyses without re-calling the LLM."""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, unique=True)
    overall_risk = Column(String(20), nullable=False)
    result_json = Column(Text, nullable=False)  # full AnalysisResult as JSON
    created_at = Column(DateTime, default=_now)

    document = relationship("Document", back_populates="analysis")
