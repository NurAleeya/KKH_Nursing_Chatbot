import os
import requests

class OpenRouterLLM:
    """Custom LLM wrapper for OpenRouter API"""
    def __init__(self, model_name="mistralai/mistral-7b-instruct"):
        self.model_name = model_name
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        if not self.api_key:
            print("Warning: OPENROUTER_API_KEY not found in environment variables")
        
    def __call__(self, prompt, **kwargs):
        if not self.api_key:
            return "I'm sorry, but the AI service is not properly configured. Please contact the administrator."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://kkh-nursing-chatbot-v2.fly.dev",
            "X-Title": "KKH Nursing Chatbot"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 1000),
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            return "I'm sorry, but the response is taking too long. Please try again."
        except requests.exceptions.RequestException as e:
            return f"I'm experiencing connection issues. Please try again later."
        except Exception as e:
            return "I'm sorry, but I encountered an unexpected error. Please try again."

class NursingChatbot:
    def __init__(self):
        # Initialize LLM with OpenRouter
        self.llm = OpenRouterLLM()
        
        # Embeddings will be initialized later when needed for vector store integration
        self.embeddings = None
        
    def ask(self, question: str, chat_history: list = None):
        """Ask a question to the chatbot."""
        # Create a context-aware prompt
        context = """You are a nursing assistant chatbot for KK Women's and Children's Hospital. 
        Provide helpful, accurate medical information and guidance for healthcare professionals.
        Focus on clinical guidelines, patient care protocols, and medical procedures.
        Always emphasize the importance of following hospital protocols and consulting with senior staff when needed."""
        
        if chat_history:
            # Add chat history to context (limit to last 3 exchanges)
            history_context = "\n".join([f"Q: {item.get('question', '')} A: {item.get('answer', '')}" for item in chat_history[-3:]])
            context += f"\n\nRecent conversation:\n{history_context}"
        
        prompt = f"{context}\n\nCurrent question: {question}\n\nPlease provide a helpful, professional response:"
        
        try:
            response = self.llm(prompt)
            return response
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. If the problem persists, please contact IT support."

# Future enhancement: Knowledge base integration
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# def load_knowledge_base():
#     """Load the knowledge base from the extracted text file."""
#     embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     knowledge_base = FAISS.load_local("data/medical_emergencies.txt", embedding_model)
#     return knowledge_base