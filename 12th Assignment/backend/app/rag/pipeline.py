import math
from typing import List, Dict, Any, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.vectorstore.faiss_store import FAISSVectorStoreManager
from app.prompts.templates import SYSTEM_PROMPT, USER_PROMPT
from app.utils.cost_calculator import calculate_llm_cost, calculate_embedding_cost
from app.config import settings

class RAGPipeline:
    @staticmethod
    def calculate_confidence_score(distances: List[float]) -> float:
        if not distances:
            return 0.0
        # Convert FAISS L2 distance to confidence score between 0.0 and 1.0
        avg_dist = float(sum(distances) / len(distances))
        score = 1.0 / (1.0 + avg_dist)
        return round(float(min(max(score, 0.0), 1.0)), 4)

    @classmethod
    def query(
        cls,
        query: str,
        document_ids: List[str],
        doc_names_map: Dict[str, str],
        top_k: int = 5
    ) -> Dict[str, Any]:
        # 1. Similarity search
        results = FAISSVectorStoreManager.similarity_search_with_score(
            document_ids=document_ids,
            query=query,
            k=top_k
        )

        if not results:
            return {
                "answer": "I couldn't find this information in the uploaded document.",
                "confidence_score": 0.0,
                "retrieved_chunk_count": 0,
                "source_pages": [],
                "sources": [],
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_cost": 0.0
            }

        context_blocks = []
        sources = []
        distances = []
        source_pages = set()

        for doc, dist in results:
            meta = doc.metadata
            page = meta.get("page", 1)
            doc_id = meta.get("document_id", "")
            doc_name = doc_names_map.get(doc_id, meta.get("document_name", "Document"))
            
            source_pages.add(page)
            distances.append(dist)
            
            chunk_info = {
                "chunk_id": meta.get("chunk_id", ""),
                "page": page,
                "content": doc.page_content,
                "score": round(float(1.0 / (1.0 + float(dist))), 4),
                "document_id": doc_id,
                "document_name": doc_name
            }
            sources.append(chunk_info)
            context_blocks.append(f"[Document: {doc_name} | Page {page}]\n{doc.page_content}")

        context_str = "\n\n".join(context_blocks)
        confidence = cls.calculate_confidence_score(distances)

        # 2. Generate LLM Answer
        system_content = SYSTEM_PROMPT.format(context=context_str)
        user_content = USER_PROMPT.format(query=query)

        llm_kwargs = {
            "model": settings.LLM_MODEL,
            "openai_api_key": settings.OPENAI_API_KEY,
            "temperature": 0.1
        }
        if settings.OPENAI_API_BASE:
            llm_kwargs["openai_api_base"] = settings.OPENAI_API_BASE

        llm = ChatOpenAI(**llm_kwargs)

        response = llm.invoke([
            SystemMessage(content=system_content),
            HumanMessage(content=user_content)
        ])

        # Token usage & Cost estimation
        token_usage = response.response_metadata.get("token_usage", {})
        prompt_tokens = token_usage.get("prompt_tokens", len(context_str.split()) * 2)
        completion_tokens = token_usage.get("completion_tokens", len(response.content.split()) * 2)
        
        cost = calculate_llm_cost(prompt_tokens, completion_tokens)

        return {
            "answer": response.content,
            "confidence_score": confidence,
            "retrieved_chunk_count": len(sources),
            "source_pages": sorted(list(source_pages)),
            "sources": sources,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_cost": cost
        }

    @classmethod
    async def query_stream(
        cls,
        query: str,
        document_ids: List[str],
        doc_names_map: Dict[str, str],
        top_k: int = 5
    ) -> AsyncGenerator[str, None]:
        results = FAISSVectorStoreManager.similarity_search_with_score(
            document_ids=document_ids,
            query=query,
            k=top_k
        )

        if not results:
            yield "I couldn't find this information in the uploaded document."
            return

        context_blocks = []
        for doc, dist in results:
            meta = doc.metadata
            page = meta.get("page", 1)
            doc_id = meta.get("document_id", "")
            doc_name = doc_names_map.get(doc_id, meta.get("document_name", "Document"))
            context_blocks.append(f"[Document: {doc_name} | Page {page}]\n{doc.page_content}")

        context_str = "\n\n".join(context_blocks)
        system_content = SYSTEM_PROMPT.format(context=context_str)
        user_content = USER_PROMPT.format(query=query)

        llm_kwargs = {
            "model": settings.LLM_MODEL,
            "openai_api_key": settings.OPENAI_API_KEY,
            "temperature": 0.1,
            "streaming": True
        }
        if settings.OPENAI_API_BASE:
            llm_kwargs["openai_api_base"] = settings.OPENAI_API_BASE

        llm = ChatOpenAI(**llm_kwargs)

        async for chunk in llm.astream([
            SystemMessage(content=system_content),
            HumanMessage(content=user_content)
        ]):
            if chunk.content:
                yield chunk.content
