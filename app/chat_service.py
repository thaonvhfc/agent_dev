import ollama
from typing import List, Tuple
from langchain.schema import Document
from sqlalchemy.orm import Session
from app.config import settings
from app.vector_store import VectorStore
from app.database import ChatHistory

class ChatService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)
        
    def _create_context_from_docs(self, docs: List[Document]) -> str:
        """Tạo context từ danh sách documents"""
        context_parts = []
        for doc in docs:
            source = doc.metadata.get('source', 'Unknown')
            content = doc.page_content.strip()
            context_parts.append(f"[Nguồn: {source}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """Tạo prompt cho model"""
        prompt = f"""Bạn là một trợ lý AI thông minh, chuyên trả lời câu hỏi dựa trên các tài liệu được cung cấp.

NGUYÊN TẮC QUAN TRỌNG:
- Chỉ trả lời dựa trên thông tin có trong các tài liệu được cung cấp
- Nếu không tìm thấy thông tin liên quan, hãy nói rõ "Tôi không tìm thấy thông tin này trong tài liệu"
- Trả lời bằng tiếng Việt một cách tự nhiên và dễ hiểu
- Nếu có thể, hãy trích dẫn nguồn thông tin

TÀI LIỆU THAM KHẢO:
{context}

CÂU HỎI: {question}

TRẢ LỜI:"""
        return prompt
    
    def chat(self, message: str, user_id: int = None, db: Session = None) -> Tuple[str, List[str]]:
        """Xử lý tin nhắn chat và trả về câu trả lời cùng nguồn"""
        try:
            # Tìm kiếm documents liên quan
            relevant_docs = self.vector_store.similarity_search(message, k=4)
            
            if not relevant_docs:
                answer = "Tôi không tìm thấy thông tin liên quan trong các tài liệu đã tải lên. Vui lòng tải lên tài liệu PDF chứa thông tin bạn cần."
                sources = []
            else:
                # Tạo context từ documents
                context = self._create_context_from_docs(relevant_docs)
                
                # Tạo prompt
                prompt = self._create_prompt(message, context)
                
                # Gọi Ollama API
                response = self.client.chat(
                    model=settings.OLLAMA_MODEL,
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    options={
                        'temperature': 0.1,
                        'top_p': 0.8,
                        'num_predict': 512
                    }
                )
                
                answer = response['message']['content'].strip()
                
                # Lấy danh sách nguồn
                sources = list(set([doc.metadata.get('source', 'Unknown') for doc in relevant_docs]))
            
            # Lưu lịch sử chat nếu có user_id và db session
            if user_id and db:
                source_file = sources[0] if sources else None
                chat_history = ChatHistory(
                    user_id=user_id,
                    question=message,
                    answer=answer,
                    source_file=source_file
                )
                db.add(chat_history)
                db.commit()
            
            return answer, sources
            
        except Exception as e:
            return f"Lỗi khi xử lý câu hỏi: {str(e)}", []