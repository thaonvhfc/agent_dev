import os
from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import settings

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Trích xuất văn bản từ file PDF"""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Lỗi khi đọc file PDF: {str(e)}")
    
    def split_text_into_chunks(self, text: str, source: str) -> List[Document]:
        """Chia văn bản thành các chunk nhỏ"""
        chunks = self.text_splitter.split_text(text)
        documents = []
        
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": source,
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            )
            documents.append(doc)
        
        return documents
    
    def process_pdf(self, file_path: str) -> List[Document]:
        """Xử lý file PDF và trả về danh sách documents"""
        text = self.extract_text_from_pdf(file_path)
        filename = os.path.basename(file_path)
        documents = self.split_text_into_chunks(text, filename)
        return documents