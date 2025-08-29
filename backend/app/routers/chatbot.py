from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from chatbot import get_chatbot_response  

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    detected_language: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer, detected_lang = get_chatbot_response(request.question)
    return ChatResponse(answer=answer, detected_language=detected_lang)

@router.get("/")
async def root():
    return {"message": "🌱 AgriTwin Chatbot router is active 🚀"}
