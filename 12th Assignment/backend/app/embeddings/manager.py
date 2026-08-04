from typing import List
from langchain_core.embeddings import Embeddings
from openai import OpenAI
from app.config import settings

class NvidiaOpenAIEmbeddings(Embeddings):
    def __init__(self, model: str, api_key: str, api_base: str):
        self.model = model
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model,
            extra_body={"input_type": "passage"} if "nv-embed-v1" not in self.model else {}
        )
        return [data.embedding for data in response.data]

    def embed_query(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=[text],
            model=self.model,
            extra_body={"input_type": "query"} if "nv-embed-v1" not in self.model else {}
        )
        return response.data[0].embedding

def get_embedding_model(model_name: str = None) -> Embeddings:
    selected_model = model_name or settings.EMBEDDING_MODEL
    api_key = settings.OPENAI_API_KEY if settings.OPENAI_API_KEY else "dummy-key-for-init"
    
    if settings.OPENAI_API_BASE:
        return NvidiaOpenAIEmbeddings(
            model=selected_model,
            api_key=api_key,
            api_base=settings.OPENAI_API_BASE
        )
        
    from langchain_openai import OpenAIEmbeddings
    return OpenAIEmbeddings(
        model=selected_model,
        openai_api_key=api_key
    )
