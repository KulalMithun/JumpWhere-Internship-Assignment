from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import get_db
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.auth_service import get_current_user
from app.rag.pipeline import RAGPipeline
from app.database.models import User, Document

router = APIRouter(prefix="/chat", tags=["Chat & RAG"])

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ChatService.process_chat(
        db=db,
        user=current_user,
        query=request.message,
        document_ids=request.document_ids,
        session_id=request.session_id,
        top_k=request.top_k
    )

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not request.document_ids:
        user_docs_res = await db.execute(select(Document).where(Document.owner_id == current_user.id))
        user_docs = user_docs_res.scalars().all()
        target_doc_ids = [d.id for d in user_docs]
        doc_map = {d.id: d.filename for d in user_docs}
    else:
        user_docs_res = await db.execute(
            select(Document).where((Document.id.in_(request.document_ids)) & (Document.owner_id == current_user.id))
        )
        user_docs = user_docs_res.scalars().all()
        target_doc_ids = [d.id for d in user_docs]
        doc_map = {d.id: d.filename for d in user_docs}

    generator = RAGPipeline.query_stream(
        query=request.message,
        document_ids=target_doc_ids,
        doc_names_map=doc_map,
        top_k=request.top_k
    )
    return StreamingResponse(generator, media_type="text/event-stream")
