from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []
    context: str
    
class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ChatHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    source_file: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    context: str
    question: str
    answer: str
    score: str  # 'like' hoặc 'unlike'

class FeedbackResponse(BaseModel):
    id: int
    user_id: int
    context: str
    question: str
    answer: str
    score: str
    created_at: datetime

    class Config:
        from_attributes = True

