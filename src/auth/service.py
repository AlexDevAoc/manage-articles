import os
from fastapi import Header, HTTPException, status


API_KEY = os.getenv("API_KEY", "default_key")

def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )