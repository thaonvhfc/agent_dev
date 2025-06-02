#!/usr/bin/env python3
"""
Mock Ollama server để demo ứng dụng
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI()

class ChatRequest(BaseModel):
    model: str
    messages: list
    options: dict = {}

class ChatResponse(BaseModel):
    message: dict
    done: bool = True

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Mock chat endpoint"""
    user_message = request.messages[-1]["content"] if request.messages else ""
    
    # Tạo câu trả lời mock dựa trên nội dung
    msg_lower = user_message.lower()
    
    if "xin chào" in msg_lower:
        response_text = "Xin chào! Tôi là trợ lý AI của bạn. Tôi có thể giúp bạn trả lời các câu hỏi dựa trên tài liệu PDF đã tải lên."
    elif "ứng dụng" in msg_lower and "ai" in msg_lower:
        response_text = "AI có nhiều ứng dụng quan trọng:\n\n**Trong Y tế:**\n- Chẩn đoán hình ảnh y khoa\n- Phát hiện sớm bệnh tật\n- Phát triển thuốc mới\n\n**Trong Giáo dục:**\n- Hệ thống học tập cá nhân hóa\n- Chatbot hỗ trợ học tập\n- Đánh giá tự động\n\n**Trong Kinh doanh:**\n- Phân tích dữ liệu khách hàng\n- Tự động hóa quy trình\n- Dự đoán xu hướng thị trường"
    elif "loại" in msg_lower and "ai" in msg_lower:
        response_text = "Có 2 loại AI chính:\n\n**AI Hẹp (Narrow AI):**\nAI hẹp được thiết kế để thực hiện một nhiệm vụ cụ thể. Ví dụ:\n- Hệ thống nhận dạng giọng nói\n- Thuật toán đề xuất trên mạng xã hội\n- Chatbot dịch vụ khách hàng\n\n**AI Tổng quát (General AI):**\nAI tổng quát có khả năng thực hiện bất kỳ nhiệm vụ trí tuệ nào mà con người có thể làm. Hiện tại, loại AI này vẫn đang trong giai đoạn nghiên cứu và phát triển."
    elif "python" in msg_lower and ("ưu điểm" in msg_lower or "ai" in msg_lower):
        response_text = "Python là ngôn ngữ lập trình phổ biến nhất trong lĩnh vực AI vì:\n- Cú pháp đơn giản, dễ học\n- Thư viện phong phú (TensorFlow, PyTorch, scikit-learn)\n- Cộng đồng lớn và tài liệu phong phú\n- Tích hợp tốt với các công cụ khoa học dữ liệu"
    elif "python" in msg_lower:
        response_text = "Python là một ngôn ngữ lập trình bậc cao, dễ học và mạnh mẽ. Nó được sử dụng rộng rãi trong phát triển web, khoa học dữ liệu, và trí tuệ nhân tạo."
    elif "fastapi" in msg_lower:
        response_text = "FastAPI là framework Python hiện đại để xây dựng API:\n- Hiệu suất cao, nhanh chóng\n- Hỗ trợ type hints\n- Tự động tạo documentation\n- Dễ dàng triển khai các model AI"
    elif "ai" in msg_lower or "trí tuệ nhân tạo" in msg_lower:
        response_text = "Trí tuệ nhân tạo (AI) là một lĩnh vực của khoa học máy tính tập trung vào việc tạo ra các hệ thống có thể thực hiện các nhiệm vụ thường đòi hỏi trí thông minh của con người. Những nhiệm vụ này bao gồm học tập, suy luận, nhận thức, hiểu ngôn ngữ tự nhiên và giải quyết vấn đề."
    else:
        response_text = f"Dựa trên tài liệu đã tải lên, tôi hiểu bạn đang hỏi về: '{user_message}'. Đây là câu trả lời được tạo từ nội dung tài liệu liên quan."
    
    return ChatResponse(
        message={
            "role": "assistant",
            "content": response_text
        }
    )

@app.get("/api/tags")
async def list_models():
    """Mock endpoint để list models"""
    return {
        "models": [
            {
                "name": "llama3.1:8b",
                "modified_at": "2024-01-01T00:00:00Z",
                "size": 4661224676
            }
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Mock Ollama Server...")
    print("📍 Server will be available at: http://localhost:11434")
    print("🔧 This is a mock server for demo purposes")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=11434,
        log_level="info"
    )