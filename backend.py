import os
import PyPDF2
from sentence_transformers import SentenceTransformer

# Load the embedding model
embedding_model = SentenceTransformer('intfloat/e5-small-v2')

# Function to process the attached file
def process_file(file_path):
    if not os.path.exists(file_path):
        return "File not found."
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            content = "\n".join(page.extract_text() for page in reader.pages)
        return content
    except Exception as e:
        return f"Error processing file: {e}"

# Function to match user query with file content
def match_query_with_file(query, file_content):
    query_embedding = embedding_model.encode(query)
    file_embedding = embedding_model.encode(file_content)
    similarity_score = query_embedding.dot(file_embedding) / (query_embedding.norm() * file_embedding.norm())
    return similarity_score
