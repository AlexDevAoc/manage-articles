from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..repositories import article as article_repo
from .models import Article, CreateArticle, UpdateArticle
from ..exceptions import ArticleNotFoundError, ArticleCreationError, ArticleConflictError
from src.cache import get_article_cache, set_article_cache, DEFAULT_TTL


def create_article(db: Session, payload: CreateArticle) -> Article:
    try:
        return article_repo.create(db, payload)
    except IntegrityError as e:
        constraint_name = getattr(getattr(e.orig, 'diag', None), 'constraint_name', None)
        if constraint_name == 'uq_article_title_author' or 'uq_article_title_author' in str(e):
            raise ArticleConflictError("An article with the same title by this author already exists.")
        
        raise ArticleCreationError(str(e))

def get_article(db: Session, article_id: int, cache_ttl: int = DEFAULT_TTL) -> Optional[Article]:
    cached = get_article_cache(article_id)
    if cached:
        return Article(**cached)

    article = article_repo.get_by_id(db, article_id)
    if not article:
        raise ArticleNotFoundError(article_id)
    set_article_cache(article_id, article.dict(), ttl=cache_ttl)
    return article

def update_article(db: Session, article_id: int, payload: UpdateArticle) -> Optional[Article]:
    article = article_repo.get_by_id(db, article_id)
    if not article:
        raise ArticleNotFoundError(article_id)
    return article_repo.update(db, article_id, payload)

def delete_article(db: Session, article_id: int) -> bool:
    article = article_repo.get_by_id(db, article_id)
    if not article:
        raise ArticleNotFoundError(article_id)
    return article_repo.delete(db, article_id)

def list_articles(
    db: Session,
    author: Optional[str] = None,
    tag: Optional[str] = None,
    order: str = "desc",
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
