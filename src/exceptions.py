
from fastapi import HTTPException


class ArticleError(HTTPException):
    """Base exception for todo-related errors"""
    pass

class ArticleNotFoundError(ArticleError):
    def __init__(self, article_id=None):
        message = "Article not found" if article_id is None else f"Article with id {article_id} not found"
        super().__init__(status_code=404, detail=message)

class ArticleCreationError(ArticleError):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to create Article: {error}")


class ArticleConflictError(ArticleError):
    def __init__(self, error: str = "Conflict: resource already exists"):
        super().__init__(status_code=409, detail=error)