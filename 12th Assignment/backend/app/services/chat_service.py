from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.database.models import ChatSession, ChatMessage, Document, User
from app.rag.pipeline import RAGPipeline

class ChatService:
    @classmethod
    async def get_or_create_session(
        cls,
        db: AsyncSession,
        user_id: str,
        session_id: Optional[str] = None,
        first_query: str = ""
    ) -> ChatSession:
        if session_id:
            result = await db.execute(
                select(ChatSession)
                .options(selectinload(ChatSession.messages))
                .where((ChatSession.id == session_id) & (ChatSession.user_id == user_id))
            )
            session = result.scalars().first()
            if session:
                return session

        # Create new session if none provided or found
        title = first_query[:40] + ("..." if len(first_query) > 40 else "") if first_query else "New Conversation"
        new_session = ChatSession(
            user_id=user_id,
            title=title
        )
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        return new_session

    @classmethod
    async def process_chat(
        cls,
        db: AsyncSession,
        user: User,
        query: str,
        document_ids: Optional[List[str]] = None,
        session_id: Optional[str] = None,
        top_k: int = 5
    ) -> dict:
        # Get target documents
        if not document_ids:
            # If no document specified, grab all user's documents
            user_docs_res = await db.execute(select(Document).where(Document.owner_id == user.id))
            user_docs = user_docs_res.scalars().all()
            target_doc_ids = [d.id for d in user_docs]
            doc_map = {d.id: d.filename for d in user_docs}
        else:
            user_docs_res = await db.execute(
                select(Document).where((Document.id.in_(document_ids)) & (Document.owner_id == user.id))
            )
            user_docs = user_docs_res.scalars().all()
            target_doc_ids = [d.id for d in user_docs]
            doc_map = {d.id: d.filename for d in user_docs}

        if not target_doc_ids:
            raise HTTPException(
                status_code=400,
                detail="No accessible documents selected for search. Please upload a document first."
            )

        session = await cls.get_or_create_session(db, user.id, session_id, first_query=query)

        # Save user prompt
        user_msg = ChatMessage(
            session_id=session.id,
            sender="user",
            content=query
        )
        db.add(user_msg)
        await db.commit()

        # Run RAG Query
        rag_res = RAGPipeline.query(
            query=query,
            document_ids=target_doc_ids,
            doc_names_map=doc_map,
            top_k=top_k
        )

        primary_doc_id = target_doc_ids[0] if len(target_doc_ids) == 1 else None

        # Save assistant message
        asst_msg = ChatMessage(
            session_id=session.id,
            document_id=primary_doc_id,
            sender="assistant",
            content=rag_res["answer"],
            confidence_score=rag_res["confidence_score"],
            sources=rag_res["sources"],
            prompt_tokens=rag_res["prompt_tokens"],
            completion_tokens=rag_res["completion_tokens"],
            total_cost=rag_res["total_cost"]
        )
        db.add(asst_msg)
        await db.commit()
        await db.refresh(asst_msg)

        return {
            "session_id": session.id,
            "message_id": asst_msg.id,
            "answer": rag_res["answer"],
            "confidence_score": rag_res["confidence_score"],
            "retrieved_chunk_count": rag_res["retrieved_chunk_count"],
            "source_pages": rag_res["source_pages"],
            "sources": rag_res["sources"],
            "prompt_tokens": rag_res["prompt_tokens"],
            "completion_tokens": rag_res["completion_tokens"],
            "total_cost": rag_res["total_cost"]
        }

    @classmethod
    async def get_user_chat_history(cls, db: AsyncSession, user_id: str) -> List[ChatSession]:
        result = await db.execute(
            select(ChatSession)
            .options(selectinload(ChatSession.messages))
            .where(ChatSession.user_id == user_id)
            .order_by(ChatSession.updated_at.desc())
        )
        return result.scalars().all()
