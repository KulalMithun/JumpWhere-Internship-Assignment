from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.schemas import DocumentResponse, DocumentRename
from app.services.doc_service import DocumentService
from app.services.auth_service import get_current_user
from app.database.models import User

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await DocumentService.process_and_save_document(db, file, current_user)

@router.get("", response_model=List[DocumentResponse])
async def get_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await DocumentService.get_user_documents(db, current_user.id)

@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await DocumentService.delete_document(db, document_id, current_user.id)
    return {"message": "Document deleted successfully"}

@router.put("/{document_id}/rename", response_model=DocumentResponse)
async def rename_document(
    document_id: str,
    payload: DocumentRename,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await DocumentService.rename_document(db, document_id, payload.filename, current_user.id)
