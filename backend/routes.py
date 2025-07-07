from fastapi import APIRouter
from backend.chatbot import NursingChatbot

router = APIRouter()
chatbot = NursingChatbot()

@router.post("/ask")
def ask_question(question: str, chat_history: list):
    """Endpoint to ask a question to the chatbot."""
    response = chatbot.ask(question, chat_history)
    return {"response": response}
