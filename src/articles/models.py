from pydantic import BaseModel, ConfigDict
from datetime import datetime

class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class Article(OrmModel):
    id: int
    title: str
    body: str
    tags: list[str] | None = None
    author: str
    published_at: datetime
    created_at: datetime
    updated_at: datetime | None = None

class CreateArticle(BaseModel):
    title: str
    body: str
    tags: list[str] | None = None 
    author: str
    published_at: datetime

class UpdateArticle(CreateArticle):
    pass