from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.chatbot.backend.chatbot import get_chatbot_response

# ✅ Router with prefix and tag
router = APIRouter(prefix="/chat", tags=["chatbot"])

# ✅ Request schema
class ChatRequest(BaseModel):
    question: str

# ✅ Response schema
class ChatResponse(BaseModel):
    answer: str
    detected_language: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer, detected_lang = get_chatbot_response(request.question)
    return {"answer": answer, "detected_language": detected_lang}

@router.get("/")  # health check
async def root():
    return {"message": "🌱 AgriTwin Chatbot API is running 🚀"}
