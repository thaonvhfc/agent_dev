# Chatbot RAG - Vietnamese PDF Q&A

A smart chatbot application using Retrieval-Augmented Generation (RAG) to answer questions from PDF content in Vietnamese.

## Features

- 📄 **Upload PDF**: Upload and process PDF files
- 🗑️ **Delete PDF (admin only)**: Delete PDF files and related data in ChromaDB
- 🤖 **Smart Chat**: Ask questions based on PDF content
- 🇻🇳 **Vietnamese Support**: Full Vietnamese interface and processing
- 🔍 **RAG Technology**: Accurate information retrieval and extraction
- 🚀 **Ollama Integration**: Use local AI model via Ollama

## Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **AI Model**: Ollama (Llama 3.1)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (multilingual)
- **PDF Processing**: PyPDF
- **Frontend**: HTML, CSS, JavaScript, Bootstrap

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Install and run Ollama

```bash
# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# Download Llama 3.1 model
ollama pull llama3.1:8b

# Start Ollama server
ollama serve
```

### 3. Configuration

Edit the `.env` file if needed:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
UPLOAD_DIRECTORY=./uploads
MAX_FILE_SIZE=10485760
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Run the application

```bash
python run.py
```

Or:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 12000 --reload
```

Access: http://localhost:12000

## Usage

1. **Upload PDF**: Drag and drop or click to select a PDF file
2. **Wait for processing**: The system will split and store the content
3. **Ask questions**: Enter your question about the PDF content
4. **Get answers**: The AI will answer based on the uploaded content
5. **Delete PDF (admin only)**: Click the 🗑️ button next to a PDF file to delete both the file and related data

## Project Structure

```
agent_dev/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main FastAPI app
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   ├── document_processor.py # PDF processing
│   ├── vector_store.py      # Vector database
│   └── chat_service.py      # Chat logic
├── static/
│   ├── style.css           # CSS styles
│   └── script.js           # JavaScript
├── templates/
│   └── dashboard.html      # Main UI
├── uploads/                # PDF storage
├── data/                   # Database folder
├── requirements.txt        # Dependencies
├── .env                    # Environment config
├── run.py                  # App runner
└── README_EN.md            # This document
```

## API Endpoints

- `GET /`: Home page
- `POST /upload`: Upload PDF file
- `POST /chat`: Send chat message
- `GET /health`: Service health check
- `GET /api/files`: Get list of uploaded PDF files
- `DELETE /api/files/{filename}`: Delete PDF file and related documents (admin only)

## Notes

- Make sure Ollama server is running before starting the application
- Maximum PDF file size: 10MB
- Only PDF files are supported (password-protected PDFs are not supported)
- When deleting a PDF, all related data in ChromaDB will also be deleted (admin only)
- The first run may take time to download the embedding model

## Troubleshooting

### Ollama connection error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve
```

### Memory error
- Reduce CHUNK_SIZE in .env
- Use a smaller model (llama3.1:7b instead of 8b)

### Vietnamese encoding error
- Make sure the PDF file uses UTF-8 encoding
- Check Vietnamese fonts in the PDF
