from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI

class NursingChatbot:
    def __init__(self):
        # Initialize embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Initialize vector store
        self.vector_store = FAISS.load_local("faiss_index", self.embeddings)

        # Initialize LLM
        self.llm = OpenAI(model="llm phi-2")

        # Create conversational retrieval chain
        self.chain = ConversationalRetrievalChain(
            retriever=self.vector_store.as_retriever(),
            llm=self.llm
        )

    def ask(self, question: str, chat_history: list):
        """Ask a question to the chatbot."""
        response = self.chain.run(question=question, chat_history=chat_history)
        return response

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
