from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings

class DocumentChunker:
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def create_chunks(
        self,
        extracted_pages: List[Dict[str, Any]],
        document_id: str,
        filename: str,
        owner_id: str
    ) -> List[Document]:
        documents = []
        chunk_counter = 0
        for page_info in extracted_pages:
            page_num = page_info["page"]
            page_text = page_info["content"]
            
            raw_chunks = self.splitter.split_text(page_text)
            for chunk_text in raw_chunks:
                chunk_counter += 1
                metadata = {
                    "chunk_id": f"{document_id}_chunk_{chunk_counter}",
                    "document_id": document_id,
                    "document_name": filename,
                    "page": page_num,
                    "owner_id": owner_id
                }
                documents.append(Document(page_content=chunk_text, metadata=metadata))
        return documents
