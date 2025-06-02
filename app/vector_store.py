import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from app.config import settings

class VectorStore:
    def __init__(self):
        # Sử dụng multilingual embedding model cho tiếng Việt
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                model_kwargs={'device': 'cpu'}
            )
        except Exception as e:
            print(f"Warning: Could not load HuggingFace embeddings: {e}")
            # Fallback to a simple embedding
            from langchain_community.embeddings import FakeEmbeddings
            self.embeddings = FakeEmbeddings(size=384)
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        
        # Khởi tạo Chroma vector store
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY
        )
    
    def add_documents(self, documents: List[Document]) -> int:
        """Thêm documents vào vector store"""
        try:
            self.vectorstore.add_documents(documents)
            self.vectorstore.persist()
            return len(documents)
        except Exception as e:
            raise Exception(f"Lỗi khi thêm documents: {str(e)}")
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Tìm kiếm documents tương tự với query"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            raise Exception(f"Lỗi khi tìm kiếm: {str(e)}")
    
    def get_retriever(self, k: int = 4):
        """Trả về retriever để sử dụng với chain"""
        return self.vectorstore.as_retriever(search_kwargs={"k": k})