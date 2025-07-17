from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.chatbot import NursingChatbot
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List] = []

router = APIRouter()
chatbot = NursingChatbot()

@router.post("/ask")
def ask_question(request: ChatRequest):
    """Endpoint to ask a question to the chatbot."""
    try:
        response = chatbot.ask(request.question, request.chat_history)
        return {"response": response, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Nursing Chatbot API is running"}
