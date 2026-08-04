import os
import shutil
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import UploadFile, HTTPException, status
from app.database.models import Document, User
from app.rag.extractor import DocumentExtractor
from app.rag.chunker import DocumentChunker
from app.vectorstore.faiss_store import FAISSVectorStoreManager
from app.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}

class DocumentService:
    @classmethod
    async def process_and_save_document(
        cls,
        db: AsyncSession,
        file: UploadFile,
        user: User
    ) -> Document:
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()

        # 1. Validate file extension
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type '{ext}'. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # 2. Save temporary upload file
        user_upload_dir = os.path.join(settings.UPLOADS_DIR, user.id)
        os.makedirs(user_upload_dir, exist_ok=True)
        file_path = os.path.join(user_upload_dir, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(file_path)
        
        # Validate file size
        if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB}MB"
            )

        doc_record = Document(
            filename=filename,
            file_path=file_path,
            file_type=ext,
            file_size=file_size,
            owner_id=user.id
        )
        db.add(doc_record)
        await db.commit()
        await db.refresh(doc_record)

        try:
            # 3. Extract text
            extracted_pages = DocumentExtractor.extract_document(file_path, ext)
            if not extracted_pages:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No readable text could be extracted from the document."
                )

            # 4. Chunk text
            chunker = DocumentChunker()
            chunks = chunker.create_chunks(
                extracted_pages=extracted_pages,
                document_id=doc_record.id,
                filename=filename,
                owner_id=user.id
            )

            # 5. Create vector store index
            FAISSVectorStoreManager.create_and_save_index(
                document_id=doc_record.id,
                docs=chunks
            )

            # 6. Update document metadata in DB
            doc_record.chunk_count = len(chunks)
            doc_record.vector_store_path = FAISSVectorStoreManager.get_index_path(doc_record.id)
            await db.commit()
            await db.refresh(doc_record)

            return doc_record

        except Exception as e:
            # Rollback file and DB record on failure
            if os.path.exists(file_path):
                os.remove(file_path)
            await db.delete(doc_record)
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process document: {str(e)}"
            )

    @classmethod
    async def get_user_documents(cls, db: AsyncSession, user_id: str) -> List[Document]:
        result = await db.execute(
            select(Document).where(Document.owner_id == user_id).order_by(Document.created_at.desc())
        )
        return result.scalars().all()

    @classmethod
    async def delete_document(cls, db: AsyncSession, document_id: str, user_id: str) -> bool:
        result = await db.execute(
            select(Document).where((Document.id == document_id) & (Document.owner_id == user_id))
        )
        doc = result.scalars().first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        # Clean file from storage
        if os.path.exists(doc.file_path):
            try:
                os.remove(doc.file_path)
            except Exception:
                pass

        # Delete vector store
        FAISSVectorStoreManager.delete_index(doc.id)

        await db.delete(doc)
        await db.commit()
        return True

    @classmethod
    async def rename_document(cls, db: AsyncSession, document_id: str, new_name: str, user_id: str) -> Document:
        result = await db.execute(
            select(Document).where((Document.id == document_id) & (Document.owner_id == user_id))
        )
        doc = result.scalars().first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        doc.filename = new_name
        await db.commit()
        await db.refresh(doc)
        return doc
