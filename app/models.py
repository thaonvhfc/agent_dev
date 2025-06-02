from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []
    
class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int