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
        prompt = f"""Bạn là một trợ lý AI chuyên nghiệp, có nhiệm vụ đọc và trả lời câu hỏi của người dùng dựa trên các đoạn văn bản đã được truy xuất.

Chỉ sử dụng thông tin từ **các đoạn văn bản được cung cấp bên dưới** để trả lời.  
Nếu không tìm thấy câu trả lời phù hợp trong các đoạn văn, hãy trả lời: **"Tôi không tìm thấy thông tin trong tài liệu."**

Yêu cầu:
- Trả lời bằng **tiếng Việt rõ ràng, chính xác**.
- Câu trả lời nên **ngắn gọn, súc tích** .
- Nếu câu trả lời có nhiều phần, hãy **đánh số** và xuống dòng các phần để dễ theo dõi.
- Tuyệt đối **không phỏng đoán** hay thêm thông tin ngoài tài liệu.
- Không nói rằng bạn là AI hoặc nhắc đến mô hình.
---

**Câu hỏi**: {question}

**Văn bản tham chiếu**:  
{context}"""
        
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
                #print(f"Context sent to Ollama API:\n{context}\n")
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
                        'temperature': 0.2,
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
            
            return answer, sources, context
            
        except Exception as e:
            return f"Lỗi khi xử lý câu hỏi: {str(e)}", []