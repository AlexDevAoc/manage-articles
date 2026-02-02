from fastapi import FastAPI
from .api import register_routes

description = """
    
    """

app = FastAPI(
    title="Manage Articles API",
    description=('Manage Articles API service for managing articles in a simple way.'
                'Public routes /health and /articles are available without authentication. '
                'Other routes require authentication via an API Key.'
                'To test in detail, clone the repository and follow the instructions in the README.md.'
                ),
    version="1.0.0"
)

register_routes(app)
