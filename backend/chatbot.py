from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
import os
import requests

class OpenRouterLLM:
    """Custom LLM wrapper for OpenRouter API"""
    def __init__(self, model_name="mistralai/mistral-7b-instruct"):
        self.model_name = model_name
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def __call__(self, prompt, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]

class NursingChatbot:
    def __init__(self):
        # Initialize embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Initialize LLM with OpenRouter
        self.llm = OpenRouterLLM()

        # For now, we'll create a simple response function
        # Vector store integration can be added later
        
    def ask(self, question: str, chat_history: list = None):
        """Ask a question to the chatbot."""
        # Create a context-aware prompt
        context = "You are a nursing assistant chatbot for KK Women's and Children's Hospital. Provide helpful, accurate medical information and guidance."
        
        if chat_history:
            # Add chat history to context
            history_context = "\n".join([f"Q: {item.get('question', '')} A: {item.get('answer', '')}" for item in chat_history[-3:]])
            context += f"\n\nRecent conversation:\n{history_context}"
        
        prompt = f"{context}\n\nCurrent question: {question}\n\nPlease provide a helpful response:"
        
        try:
            response = self.llm(prompt)
            return response
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"

def load_knowledge_base():
    """Load the knowledge base from the extracted text file."""
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    knowledge_base = FAISS.load_local("c:/Users/23050830/KKH_Nursing_Chatbot_V2/data/medical_emergencies.txt", embedding_model)
    return knowledge_base

knowledge_base = load_knowledge_base()

# Modify the chatbot logic to query the knowledge base
def query_knowledge_base(query):
    """Query the knowledge base and return relevant results."""
    results = knowledge_base.similarity_search(query, k=3)
    return results

# Example usage
if __name__ == "__main__":
    query = "What are the steps for managing a cardiac arrest?"
    response = query_knowledge_base(query)
    for idx, result in enumerate(response):
        print(f"Result {idx + 1}: {result.page_content}")
