from fastapi import APIRouter
from services.db_service import get_all_history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("")
async def list_history():
    return {"items": get_all_history()}
