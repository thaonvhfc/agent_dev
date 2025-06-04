from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []
    
class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
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