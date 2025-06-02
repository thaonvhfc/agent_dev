# PDF Chatbot RAG - Hệ thống Hỏi đáp từ PDF

Hệ thống chatbot thông minh sử dụng RAG (Retrieval-Augmented Generation) để trả lời câu hỏi từ tài liệu PDF bằng tiếng Việt.

## ✨ Tính năng

- 📄 **Tải lên PDF**: Hỗ trợ tải lên và xử lý file PDF với drag & drop
- 🔍 **Tìm kiếm thông minh**: Sử dụng vector search để tìm thông tin liên quan
- 💬 **Chat tiếng Việt**: Trả lời câu hỏi bằng tiếng Việt tự nhiên
- 🤖 **Ollama Integration**: Sử dụng Ollama server cho AI model
- ⚡ **FastAPI Backend**: API nhanh và hiệu quả
- 🎨 **Giao diện đẹp**: Web interface responsive với Bootstrap
- 📚 **RAG Pipeline**: Kết hợp retrieval và generation cho câu trả lời chính xác
- 🔄 **Real-time Chat**: Chat interface với typing indicator

## 🚀 Demo

Ứng dụng đã được test thành công với:
- ✅ Upload PDF tiếng Việt về AI
- ✅ Xử lý và phân đoạn tài liệu
- ✅ Tìm kiếm vector với ChromaDB
- ✅ Chat với câu trả lời tiếng Việt chính xác
- ✅ Giao diện responsive và thân thiện

## 📦 Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd agent_dev
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cài đặt Ollama
```bash
# Trên Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Tải model
ollama pull llama3.1:8b
```

### 4. Cấu hình
Tạo file `.env`:
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
UPLOAD_DIR=uploads
DATA_DIR=data
```

## 🏃‍♂️ Chạy ứng dụng

### Phương án 1: Sử dụng Ollama thật
```bash
# 1. Khởi động Ollama server
ollama serve

# 2. Chạy ứng dụng
python run.py
```

### Phương án 2: Sử dụng Mock Ollama (cho demo)
```bash
# 1. Chạy mock Ollama server
python mock_ollama.py &

# 2. Chạy ứng dụng
python run.py
```

Truy cập: http://localhost:12000

## 📁 Cấu trúc dự án

```
agent_dev/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app chính
│   ├── config.py            # Cấu hình
│   ├── models.py            # Data models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py  # Xử lý PDF
│   │   ├── vector_store.py        # Vector database
│   │   └── chat_service.py        # Chat logic
├── static/
│   ├── style.css           # CSS styling
│   └── script.js           # JavaScript
├── templates/
│   └── index.html          # Web interface
├── uploads/                # Thư mục upload
├── data/                   # Vector database
├── requirements.txt        # Dependencies
├── run.py                 # Entry point
├── mock_ollama.py         # Mock Ollama server
├── tai_lieu_mau.pdf       # Sample PDF
└── README.md              # Tài liệu
```

## 📖 Sử dụng

1. **Tải lên PDF**: 
   - Kéo thả file PDF vào vùng upload
   - Hoặc click để chọn file từ máy tính
   - Hỗ trợ file PDF tiếng Việt

2. **Đợi xử lý**: 
   - Hệ thống sẽ phân tích nội dung PDF
   - Chia thành các đoạn văn bản
   - Tạo vector embeddings và lưu vào ChromaDB

3. **Đặt câu hỏi**: 
   - Nhập câu hỏi về nội dung PDF
   - Hỗ trợ câu hỏi tiếng Việt tự nhiên
   - Ví dụ: "AI có những ứng dụng gì?", "Python có ưu điểm gì trong AI?"

4. **Nhận câu trả lời**: 
   - AI sẽ tìm kiếm thông tin liên quan trong tài liệu
   - Tạo câu trả lời dựa trên nội dung tìm được
   - Hiển thị nguồn tham khảo từ file PDF

## 🛠️ Công nghệ sử dụng

### Backend
- **FastAPI**: Web framework hiện đại cho Python
- **Ollama**: Local LLM server (llama3.1:8b)
- **ChromaDB**: Vector database cho similarity search
- **PyPDF**: Xử lý và trích xuất text từ PDF
- **LangChain**: Framework cho RAG pipeline

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling với Flexbox/Grid
- **JavaScript**: Interactive functionality
- **Bootstrap**: Responsive UI components
- **Font Awesome**: Icon library

### AI/ML
- **RAG (Retrieval-Augmented Generation)**: Kết hợp tìm kiếm và sinh text
- **Vector Embeddings**: Chuyển đổi text thành vector số
- **Semantic Search**: Tìm kiếm dựa trên ý nghĩa
- **Text Chunking**: Chia nhỏ tài liệu để xử lý hiệu quả

## 🔧 Cấu hình nâng cao

### Tùy chỉnh model Ollama
```python
# Trong app/config.py
OLLAMA_MODEL = "llama3.1:8b"  # Hoặc model khác
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Tùy chỉnh chunk size
```python
# Trong app/services/document_processor.py
chunk_size = 1000  # Kích thước mỗi đoạn text
chunk_overlap = 200  # Độ chồng lấp giữa các đoạn
```

### Tùy chỉnh vector store
```python
# Trong app/services/vector_store.py
collection_name = "pdf_documents"
persist_directory = "./data"
```

## 🐛 Troubleshooting

### Lỗi thường gặp

1. **Ollama không kết nối được**:
   ```bash
   # Kiểm tra Ollama đang chạy
   curl http://localhost:11434/api/tags
   
   # Khởi động lại Ollama
   ollama serve
   ```

2. **Lỗi import sentence-transformers**:
   ```bash
   # Cài đặt thêm (tùy chọn)
   pip install sentence-transformers
   ```

3. **File PDF không đọc được**:
   - Đảm bảo file PDF không bị mã hóa
   - Kiểm tra file có text layer (không phải scan)

4. **Vector store lỗi**:
   ```bash
   # Xóa và tạo lại
   rm -rf data/
   # Restart ứng dụng
   ```

## 📝 Lưu ý

- ✅ Hỗ trợ file PDF tiếng Việt
- ✅ Cần Ollama server chạy trước khi khởi động app
- ✅ Vector store sẽ được tạo tự động trong thư mục `data/`
- ✅ Ứng dụng có fallback embeddings nếu không có sentence-transformers
- ✅ Mock Ollama server có sẵn cho demo và testing

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.