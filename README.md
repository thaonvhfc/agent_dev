# Chatbot RAG - Hỏi đáp từ PDF bằng tiếng Việt

Ứng dụng chatbot thông minh sử dụng RAG (Retrieval-Augmented Generation) để trả lời câu hỏi từ nội dung file PDF bằng tiếng Việt.

## Tính năng

- 📄 **Upload PDF**: Tải lên và xử lý file PDF
- 🤖 **Chat thông minh**: Hỏi đáp dựa trên nội dung PDF
- 🇻🇳 **Hỗ trợ tiếng Việt**: Giao diện và xử lý hoàn toàn bằng tiếng Việt
- 🔍 **RAG Technology**: Tìm kiếm và trích xuất thông tin chính xác
- 🚀 **Ollama Integration**: Sử dụng model AI local qua Ollama

## Công nghệ sử dụng

- **Backend**: FastAPI, Python 3.8+
- **AI Model**: Ollama (Llama 3.1)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (multilingual)
- **PDF Processing**: PyPDF
- **Frontend**: HTML, CSS, JavaScript, Bootstrap

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cài đặt và chạy Ollama

```bash
# Cài đặt Ollama (Linux/macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# Tải model Llama 3.1
ollama pull llama3.1:8b

# Chạy Ollama server
ollama serve
```

### 3. Cấu hình

Chỉnh sửa file `.env` nếu cần:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
UPLOAD_DIRECTORY=./uploads
MAX_FILE_SIZE=10485760
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Chạy ứng dụng

```bash
python run.py
```

Hoặc:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 12000 --reload
```

Truy cập: http://localhost:12000

## Cách sử dụng

1. **Tải lên PDF**: Kéo thả hoặc click để chọn file PDF
2. **Đợi xử lý**: Hệ thống sẽ chia nhỏ và lưu trữ nội dung
3. **Đặt câu hỏi**: Nhập câu hỏi về nội dung PDF
4. **Nhận câu trả lời**: AI sẽ trả lời dựa trên nội dung đã tải

## Cấu trúc dự án

```
agent_dev/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app chính
│   ├── config.py            # Cấu hình
│   ├── models.py            # Pydantic models
│   ├── document_processor.py # Xử lý PDF
│   ├── vector_store.py      # Vector database
│   └── chat_service.py      # Logic chat
├── static/
│   ├── style.css           # CSS styles
│   └── script.js           # JavaScript
├── templates/
│   └── index.html          # Giao diện chính
├── uploads/                # Thư mục lưu PDF
├── data/                   # Thư mục database
├── requirements.txt        # Dependencies
├── .env                    # Cấu hình môi trường
├── run.py                  # Script chạy app
└── README.md              # Tài liệu này
```

## API Endpoints

- `GET /`: Trang chủ
- `POST /upload`: Upload file PDF
- `POST /chat`: Gửi tin nhắn chat
- `GET /health`: Kiểm tra sức khỏe service

## Lưu ý

- Đảm bảo Ollama server đang chạy trước khi khởi động ứng dụng
- File PDF tối đa 10MB
- Chỉ hỗ trợ file PDF (không hỗ trợ PDF được bảo vệ bằng mật khẩu)
- Lần đầu chạy có thể mất thời gian để tải embedding model

## Troubleshooting

### Lỗi kết nối Ollama
```bash
# Kiểm tra Ollama đang chạy
curl http://localhost:11434/api/tags

# Khởi động lại Ollama
ollama serve
```

### Lỗi memory
- Giảm CHUNK_SIZE trong .env
- Sử dụng model nhỏ hơn (llama3.1:7b thay vì 8b)

### Lỗi encoding tiếng Việt
- Đảm bảo file PDF có encoding UTF-8
- Kiểm tra font tiếng Việt trong PDF