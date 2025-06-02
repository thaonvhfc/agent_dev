import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

from app.models import ChatMessage, ChatResponse, UploadResponse
from app.document_processor import DocumentProcessor
from app.vector_store import VectorStore
from app.chat_service import ChatService
from app.config import settings

app = FastAPI(title="Vietnamese PDF Chatbot RAG", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files và templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Khởi tạo services
document_processor = DocumentProcessor()
vector_store = VectorStore()
chat_service = ChatService()

# Tạo thư mục uploads nếu chưa tồn tại
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Trang chủ"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload và xử lý file PDF"""
    
    # Kiểm tra định dạng file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")
    
    # Kiểm tra kích thước file
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File quá lớn (tối đa 10MB)")
    
    try:
        # Lưu file
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, file.filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Xử lý PDF
        documents = document_processor.process_pdf(file_path)
        
        # Thêm vào vector store
        chunks_created = vector_store.add_documents(documents)
        
        return UploadResponse(
            message="File đã được tải lên và xử lý thành công",
            filename=file.filename,
            chunks_created=chunks_created
        )
        
    except Exception as e:
        # Xóa file nếu có lỗi
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý file: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Xử lý tin nhắn chat"""
    try:
        response, sources = chat_service.chat(message.message)
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý chat: {str(e)}")

@app.get("/health")
async def health_check():
    """Kiểm tra sức khỏe của service"""
    return {"status": "healthy", "message": "Service đang hoạt động bình thường"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=12000,
        reload=True
    )