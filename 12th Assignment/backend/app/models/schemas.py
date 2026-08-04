from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

# User Schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Document Schemas
class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    chunk_count: int
    created_at: datetime
    owner_id: str

    class Config:
        from_attributes = True

class DocumentRename(BaseModel):
    filename: str

# Chat Schemas
class SourceChunk(BaseModel):
    chunk_id: str
    page: Optional[int] = None
    content: str
    score: float
    document_id: str
    document_name: str

class ChatRequest(BaseModel):
    message: str
    document_ids: Optional[List[str]] = None
    session_id: Optional[str] = None
    top_k: int = 5

class ChatResponse(BaseModel):
    session_id: str
    message_id: str
    answer: str
    confidence_score: float
    retrieved_chunk_count: int
    source_pages: List[int]
    sources: List[SourceChunk]
    prompt_tokens: int
    completion_tokens: int
    total_cost: float

class MessageResponse(BaseModel):
    id: str
    sender: str
    content: str
    confidence_score: Optional[float] = None
    sources: Optional[List[Any]] = None
    prompt_tokens: Optional[int] = 0
    completion_tokens: Optional[int] = 0
    total_cost: Optional[float] = 0.0
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True
