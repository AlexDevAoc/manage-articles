from typing import List, Optional
from fastapi import APIRouter, Depends

from src.repositories.article import ArticleOrder

from ..database.core import DbSession
from . import models, service
from ..auth.service import api_key_auth

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)

@router.post("", response_model=models.Article, dependencies=[Depends(api_key_auth)])
def create_article(db: DbSession, article: models.CreateArticle):
    return service.create_article(db, article)

@router.get("/{id}", response_model=models.Article, dependencies=[Depends(api_key_auth)])
def get_article(db: DbSession, id: int):
    return service.get_article(db, id)

@router.put("/{id}", response_model=models.Article, dependencies=[Depends(api_key_auth)])
def update_article(db: DbSession, id: int, article: models.UpdateArticle):
    return service.update_article(db, id, article)

@router.delete("/{id}", dependencies=[Depends(api_key_auth)])
def delete_article(db: DbSession, id: int):
    return service.delete_article(db, id)

@router.get("", response_model=List[models.Article])
def list_articles(
        db: DbSession,
        author: Optional[str] = None,
        tag: Optional[str] = None,
        order: ArticleOrder = ArticleOrder.ASC,
        limit: int = 10,
        offset: int = 0):
    return service.list_articles(db, author, tag, order, limit, offset)