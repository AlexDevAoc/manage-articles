import datetime
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import Session

from ..entities.article import Article
from ..articles import models as article_models

class ArticleOrder(str, Enum):
    """Enum for article ordering options."""
    ASC = "asc"
    DESC = "desc"

def get_by_id(db: Session, article_id: int) -> Optional[Article]:
    return db.query(Article).filter(Article.id == article_id).first()

def create(db: Session, payload: article_models.CreateArticle) -> Article:
    obj = Article(
        title=payload.title,
        body=payload.body,
        tags=payload.tags,
        author=payload.author,
        published_at=payload.published_at
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, article_id: int, payload: article_models.UpdateArticle) -> Optional[Article]:
    obj = get_by_id(db, article_id)
    if not obj:
        return None
    obj.title = payload.title
    obj.body = payload.body
    obj.tags = payload.tags
    obj.author = payload.author
    obj.published_at = payload.published_at
    obj.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, article_id: int) -> bool:
    obj = get_by_id(db, article_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def list_all(
    db: Session,
    author: Optional[str] = None,
    tag: Optional[str] = None,
    order: str = "desc",
    limit: int = 10,
    offset: int = 0
) -> List[Article]:
    query = db.query(Article)
    if author:
        query = query.filter(Article.author == author)
    if tag:
        query = query.filter(Article.tags.contains([tag]))
    # Check the order and apply the appropriate ordering
    order_clause = (
        Article.published_at.asc()
        if order == ArticleOrder.ASC
        else Article.published_at.desc()
    )
    return query.order_by(order_clause).offset(offset).limit(limit).all()