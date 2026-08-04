import os
from typing import List, Tuple, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.embeddings.manager import get_embedding_model
from app.config import settings

class FAISSVectorStoreManager:
    _cache: Dict[str, FAISS] = {}

    @classmethod
    def get_index_path(cls, document_id: str) -> str:
        return os.path.join(settings.VECTOR_STORE_DIR, document_id)

    @classmethod
    def create_and_save_index(cls, document_id: str, docs: List[Document]) -> FAISS:
        embedding_function = get_embedding_model()
        vectorstore = FAISS.from_documents(docs, embedding_function)
        index_path = cls.get_index_path(document_id)
        os.makedirs(index_path, exist_ok=True)
        vectorstore.save_local(index_path)
        cls._cache[document_id] = vectorstore
        return vectorstore

    @classmethod
    def load_index(cls, document_id: str) -> FAISS:
        if document_id in cls._cache:
            return cls._cache[document_id]
        
        index_path = cls.get_index_path(document_id)
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Vector store index for document '{document_id}' not found at {index_path}")
        
        embedding_function = get_embedding_model()
        vectorstore = FAISS.load_local(
            index_path,
            embedding_function,
            allow_dangerous_deserialization=True
        )
        cls._cache[document_id] = vectorstore
        return vectorstore

    @classmethod
    def delete_index(cls, document_id: str) -> bool:
        if document_id in cls._cache:
            del cls._cache[document_id]
        
        index_path = cls.get_index_path(document_id)
        if os.path.exists(index_path):
            import shutil
            shutil.rmtree(index_path)
            return True
        return False

    @classmethod
    def similarity_search_with_score(
        cls,
        document_ids: List[str],
        query: str,
        k: int = 5
    ) -> List[Tuple[Document, float]]:
        all_results = []
        for doc_id in document_ids:
            try:
                vs = cls.load_index(doc_id)
                results = vs.similarity_search_with_score(query, k=k)
                all_results.extend([(doc, float(score)) for doc, score in results])
            except Exception as e:
                print(f"Error loading index for {doc_id}: {str(e)}")

        # FAISS returns L2 distance or inner product. Lower distance is higher similarity.
        all_results.sort(key=lambda x: x[1])
        return all_results[:k]
