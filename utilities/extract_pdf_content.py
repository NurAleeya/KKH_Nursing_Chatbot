from PyPDF2 import PdfReader
import os
import json
from datetime import datetime

def extract_pdf_content(pdf_path):
    """Extract text content from a PDF file."""
    reader = PdfReader(pdf_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text() + "\n"
    return content

if __name__ == "__main__":
    pdf_path = "c:/Users/23050830/KKH_Nursing_Chatbot_V2/data/Section 01 - Medical Emergencies.pdf"
    output_path = "c:/Users/23050830/KKH_Nursing_Chatbot_V2/data/medical_emergencies.txt"
    chat_history_path = "c:/Users/23050830/KKH_Nursing_Chatbot_V2/data/chat_history.json"

    # Extract PDF content
    content = extract_pdf_content(pdf_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Content extracted and saved to {output_path}")