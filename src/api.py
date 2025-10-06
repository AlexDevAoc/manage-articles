from fastapi import FastAPI
from src.articles.controller import router as articles_router

def register_routes(app: FastAPI):
    app.include_router(articles_router)