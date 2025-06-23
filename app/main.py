import os
import shutil
from datetime import timedelta, datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import aiofiles

from app.models import (
    ChatMessage, ChatResponse, UploadResponse, 
    UserCreate, UserLogin, Token, UserResponse, ChatHistoryResponse
)
from app.document_processor import DocumentProcessor
from app.vector_store import VectorStore
from app.chat_service import ChatService
from app.config import settings
from app.database import get_db, create_tables, User, ChatHistory
from app.auth import (
    authenticate_user, create_access_token, get_current_user, 
    get_current_admin_user, get_password_hash, create_admin_user,
    get_current_user_required, ACCESS_TOKEN_EXPIRE_MINUTES
)

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

# Tạo database tables
create_tables()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Trang chủ - chuyển hướng đến login"""
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Trang đăng nhập"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Trang đăng ký"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard chính sau khi đăng nhập"""
    # Tạo user mặc định cho template (sẽ được override bởi JavaScript)
    default_user = {
        "username": "thao test main",
        "role": "user",
        "created_at": datetime.now(),
    }
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": default_user
    })

# Authentication endpoints
@app.post("/api/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Đăng ký user mới"""
    # Kiểm tra username đã tồn tại
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username đã tồn tại"
        )
    
    # Kiểm tra email đã tồn tại
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email đã tồn tại"
        )
    
    # Tạo user mới
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        is_admin=(user_data.role == "admin")
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/api/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Đăng nhập"""
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username hoặc password không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...), 
    current_user: User = Depends(get_current_admin_user)
):
    """Upload và xử lý file PDF - chỉ admin"""
    
    # Kiểm tra định dạng file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")
    
    # Kiểm tra kích thước file
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File quá lớn (tối đa 20MB)")
    
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
async def chat(
    message: ChatMessage, 
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Xử lý tin nhắn chat - yêu cầu đăng nhập"""
    try:
        response, sources = chat_service.chat(message.message, current_user.id, db)
        return ChatResponse(response=response, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý chat: {str(e)}")

@app.get("/api/chat-history", response_model=list[ChatHistoryResponse])
async def get_chat_history(
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Lấy lịch sử chat của user"""
    chat_history = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id
    ).order_by(ChatHistory.created_at.desc()).limit(50).all()
    
    return chat_history

@app.get("/api/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user_required)):
    """Lấy thông tin user hiện tại"""
    return current_user

@app.post("/api/logout")
async def logout():
    """Đăng xuất"""
    return {"message": "Đăng xuất thành công"}

@app.get("/api/users", response_model=list[UserResponse])
async def get_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Lấy danh sách users - chỉ admin"""
    users = db.query(User).all()
    return users

@app.get("/api/files")
async def get_uploaded_files(current_user: User = Depends(get_current_user_required)):
    """Lấy danh sách file đã upload"""
    upload_dir = settings.UPLOAD_DIRECTORY
    files = []
    
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(upload_dir, filename)
                files.append({
                    "filename": filename,
                    "size": os.path.getsize(file_path),
                    "uploaded_at": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                })
    
    return files

@app.delete("/api/files/{filename}")
async def delete_file(
    filename: str,
    current_user: User = Depends(get_current_admin_user)
):
    """Xóa file PDF và documents liên quan - chỉ admin"""
    try:
        # Kiểm tra quyền admin
        if not current_user.is_admin:
            raise HTTPException(
                status_code=403,
                detail="Chỉ admin mới có quyền xóa file"
            )

        file_path = os.path.join(settings.UPLOAD_DIRECTORY, filename)
        
        # Xóa file từ thư mục uploads
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # Xóa documents từ Chroma
        vector_store = VectorStore()
        vector_store.delete_documents_by_source(filename)
        
        return {
            "message": f"Đã xóa file {filename} và documents liên quan",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi xóa file: {str(e)}"
        )

@app.get("/health")
async def health_check(health="good"):
    """Kiểm tra sức khỏe của service"""
    print("Kiểm tra sức khỏe service: ", health)
    return {"status": "healthy", "message": "Service đang hoạt động bình thường"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=12000,
        reload=True
    )