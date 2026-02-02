from fastapi import APIRouter
from src.health.service import health_check

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)  

@router.get("")
def health_check_api():
    return health_check()