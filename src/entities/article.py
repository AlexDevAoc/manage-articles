from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY

from ..database.core import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(ARRAY(String), nullable=True)
    author = Column(String(100), nullable=False)
    published_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_article_author_published_at", "author", "published_at"),
        UniqueConstraint("title", "author", name="uq_article_title_author"),
    )