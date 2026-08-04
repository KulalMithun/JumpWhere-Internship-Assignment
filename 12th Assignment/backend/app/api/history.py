from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.schemas import ChatSessionResponse
from app.services.chat_service import ChatService
from app.services.auth_service import get_current_user
from app.database.models import User

router = APIRouter(prefix="/history", tags=["History"])

@router.get("", response_model=List[ChatSessionResponse])
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatService.get_user_chat_history(db, current_user.id)
