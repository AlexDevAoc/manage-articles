from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..repositories import article as article_repo
from .models import Article, CreateArticle, UpdateArticle
from ..exceptions import ArticleNotFoundError, ArticleCreationError, ArticleConflictError
from src.cache import get_article_cache, set_article_cache, invalidate_article_cache


def create_article(db: Session, payload: CreateArticle) -> Article:
    try:
        return article_repo.create(db, payload)
        
    except IntegrityError as e:
        constraint_name = getattr(getattr(e.orig, 'diag', None), 'constraint_name', None)
        if constraint_name == 'uq_article_title_author' or 'uq_article_title_author' in str(e):
            raise ArticleConflictError("An article with the same title by this author already exists.")
        
        raise ArticleCreationError(str(e))

def get_article(db: Session, article_id: int) -> Optional[Article]:
    cached = get_article_cache(article_id)
    if cached:
        return Article(**cached)

    article = article_repo.get_by_id(db, article_id)
    if not article:
        raise ArticleNotFoundError(article_id)
    
    article_schema = Article.model_validate(article)
    set_article_cache(article_id, article_schema)

    return article_schema

def update_article(db: Session, article_id: int, payload: UpdateArticle) -> Optional[Article]:
    article = article_repo.get_by_id(db, article_id)
    if not article:
        raise ArticleNotFoundError(article_id)
    
    updated_article = article_repo.update(db, article_id, payload)
    if updated_article:
        invalidate_article_cache(article_id)
        return Article.model_validate(updated_article)
    return None

def delete_article(db: Session, article_id: int) -> bool:
    article = article_repo.get_by_id(db, article_id)
    if not article:
        raise ArticleNotFoundError(article_id)
    
    deleted = article_repo.delete(db, article_id)
    if deleted:
        invalidate_article_cache(article_id)
    return deleted

def list_articles(
    db: Session,
    author: Optional[str] = None,
    tag: Optional[str] = None,
    order: str = "asc",
    limit: int = 10,
    offset: int = 0
) -> list[Article]:
    return article_repo.list_all(
        db,
        author=author,
        tag=tag,
        order=order,
        limit=limit,
        offset=offset
    )
