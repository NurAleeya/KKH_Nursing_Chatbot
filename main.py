import streamlit as st
import requests
import os
from sentence_transformers import SentenceTransformer
import PyPDF2
import numpy as np
import torch
import time
import random

# Explicitly set the device for the embedding model
embedding_model = SentenceTransformer('intfloat/e5-small-v2', device="cuda" if torch.cuda.is_available() else "cpu")

def check_server_availability(server_url):
    """Check if the server is reachable."""
    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            return True
        else:
            print(f"Server check failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Server availability check failed: {e}")
        return False

def query_llm(prompt):
    # Use environment variable for server URL, fallback to local development
    server_base = os.getenv("LLM_SERVER_URL", "http://10.175.5.70:1234")
    server_url = f"{server_base}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    max_retries = 3
    retry_delay = 5  # seconds

    # Check server availability before making requests
    if not check_server_availability(server_base):
        return "LLM Server is not reachable. Please check the connection or contact support."

    payload = {
        "model": "mistralai/mistral-7b-instruct-v0.3",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(server_url, json=payload, headers=headers)
            print(f"Response status: {response.status_code}")  # Debugging: Print status code
            print(f"Response headers: {response.headers}")  # Debugging: Print headers
            print(f"Response body: {response.text}")  # Debugging: Print raw response text

            if response.status_code == 200:
                llm_response = response.json()
                return llm_response.get("choices", [{}])[0].get("message", {}).get("content", "No response from LLM")
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                return f"An error occurred after {max_retries} attempts: {e}"

def calculate_fluid_requirement(weight):
    # Example formula: 100 ml/kg for the first 10 kg, 50 ml/kg for the next 10 kg, 20 ml/kg for the rest
    if weight <= 10:
        return weight * 100
    elif weight <= 20:
        return 1000 + (weight - 10) * 50
    else:
        return 1500 + (weight - 20) * 20

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
    similarity_score = np.dot(query_embedding, file_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(file_embedding))
    return similarity_score

# Function to generate MCQ quiz questions and answers
def generate_mcq_questions():
    questions_pool = [
        {
            "question": "What is the normal range for blood pressure in adults?",
            "options": ["120/80 mmHg", "140/90 mmHg", "100/70 mmHg", "160/100 mmHg"],
            "answer": "120/80 mmHg"
        },
        {
            "question": "How do you calculate BMI?",
            "options": ["Weight (kg) / Height (m)^2", "Height (m) / Weight (kg)^2", "Weight (kg) * Height (m)^2", "Height (m) * Weight (kg)^2"],
            "answer": "Weight (kg) / Height (m)^2"
        },
        {
            "question": "What are the symptoms of dehydration?",
            "options": ["Thirst, dry mouth, dark urine", "Sweating, confusion, shakiness", "Fever, rapid heart rate, confusion", "Repositioning and skin care"],
            "answer": "Thirst, dry mouth, dark urine"
        },
        {
            "question": "What is the first step in CPR?",
            "options": ["Check responsiveness", "Start chest compressions", "Call for help", "Give rescue breaths"],
            "answer": "Check responsiveness"
        },
        {
            "question": "How do you assess pain in non-verbal patients?",
            "options": ["Use pain scales or observe behavior", "Ask the patient directly", "Monitor fluid intake", "Check blood pressure"],
            "answer": "Use pain scales or observe behavior"
        },
        {
            "question": "What are the signs of hypoglycemia?",
            "options": ["Sweating, confusion, shakiness", "Thirst, dry mouth, dark urine", "Fever, rapid heart rate, confusion", "Repositioning and skin care"],
            "answer": "Sweating, confusion, shakiness"
        },
        {
            "question": "What is the recommended daily fluid intake for adults?",
            "options": ["2-3 liters", "1-2 liters", "3-4 liters", "4-5 liters"],
            "answer": "2-3 liters"
        },
        {
            "question": "How do you prevent pressure ulcers?",
            "options": ["Repositioning and skin care", "Use pain scales or observe behavior", "Monitor fluid intake", "Check blood pressure"],
            "answer": "Repositioning and skin care"
        },
        {
            "question": "What are the steps for administering an IV medication?",
            "options": ["Prepare, verify, administer", "Check responsiveness, call for help", "Start chest compressions, give rescue breaths", "Monitor fluid intake, check blood pressure"],
            "answer": "Prepare, verify, administer"
        },
        {
            "question": "What is the normal heart rate range for children?",
            "options": ["70-120 bpm", "60-100 bpm", "80-140 bpm", "50-90 bpm"],
            "answer": "70-120 bpm"
        }
    ]
    return random.sample(questions_pool, 10)

def main():
    st.set_page_config(page_title="Nursing Chatbot", page_icon="kkh_logo.png", layout="wide")
    col1, col2 = st.columns([1, 7])  # Further adjusted column width ratio to minimize gap
    with col1:
        st.image("data/KKH Logo.jpg", width=100)
    with col2:
        st.title("KK Women's and Children's Hospital")
    st.markdown("### Your 24/7 nurse assistant for clinical guidelines, calculations and education.")

    menu = ["Retrieve Clinical Guidelines", "Calculate Fluid Requirement", "Take a Quiz"]
    choice = st.sidebar.radio("Select an option:", menu)  # Removed the empty string from options

    if choice == "Retrieve Clinical Guidelines":
        st.subheader("📚 Retrieve Clinical Guidelines")

        predefined_prompts = [
            "Custom Query",
            "What are the clinical guidelines for managing hypertension?",
            "How to calculate medication dosage for pediatric patients?",
            "What are the steps for infection control in ICU?",
            "What are the best practices for wound care management?",
            "How to handle medication reconciliation during patient discharge?",
            "What are the protocols for managing diabetic ketoacidosis?",
            "How to assess and manage pain in non-verbal patients?",
            "What are the guidelines for administering blood transfusions?",
            "How to prevent and manage pressure ulcers?",
            "What are the steps for performing a sterile dressing change?"
        ]

        selected_prompt = st.sidebar.selectbox("Choose a predefined prompt:", predefined_prompts)

        if selected_prompt == "Custom Query":
            prompt = st.text_area("Enter your query for clinical guidelines:", value="", height=150)
        else:
            st.session_state.custom_query = selected_prompt
            prompt = st.text_area("Enter your query for clinical guidelines:", value=st.session_state.get("custom_query", ""), height=150)

        if st.button("Submit", key="guidelines_submit"):
            with st.spinner("Fetching response..."):
                response = query_llm(prompt)
            st.success("Response received!")
            st.write(f"### Response:\n{response}")

    elif choice == "Calculate Fluid Requirement":
        st.subheader("🧮 Calculate Fluid Requirement")
        weight = st.number_input("Enter patient weight (kg):", min_value=0.0, step=0.1)
        if st.button("Calculate", key="fluid_calculate"):
            with st.spinner("Calculating..."):
                fluid = calculate_fluid_requirement(weight)
            st.success("Calculation complete!")
            st.metric(label="Fluid Requirement (ml)", value=f"{fluid} ml")

    elif choice == "Take a Quiz":
        st.subheader("📝 Take a Quiz")

        if "quiz_questions" not in st.session_state:
            st.session_state.quiz_questions = generate_mcq_questions()

        quiz_questions = st.session_state.quiz_questions
        user_answers = {}

        for i, q in enumerate(quiz_questions, start=1):
            st.write(f"**Question {i}:** {q['question']}")
            user_answers[i] = st.radio(
                f"Choose your answer for Question {i}:",
                q['options'],
                key=f"answer_{i}",
                index=None  # Ensure no pre-selected option
            )

        if st.button("Submit Quiz", key="quiz_submit"):
            if len(user_answers) < 10:
                st.error("Please complete all 10 questions before submitting.")
            else:
                results = []
                total_marks = 0

                explanations = {
                    "What is the normal range for blood pressure in adults?": "The correct answer is '120/80 mmHg', which is considered the standard normal range for adults. Other options represent either elevated or hypotensive values that are not ideal.",
                    "How do you calculate BMI?": "The formula 'Weight (kg) / Height (m)^2' is used to calculate BMI, which assesses body fat based on weight and height. Other options are mathematically incorrect.",
                    "What are the symptoms of dehydration?": "Symptoms like 'Thirst, dry mouth, dark urine' are classic signs of dehydration. Other options include symptoms unrelated to dehydration, such as fever or confusion.",
                    "What is the first step in CPR?": "'Check responsiveness' is the first step to determine if the person needs CPR. Other options like chest compressions or rescue breaths come later in the sequence.",
                    "How do you assess pain in non-verbal patients?": "Using pain scales or observing behavior is the recommended method for assessing pain in non-verbal patients. Other options like checking blood pressure are not directly related to pain assessment.",
                    "What are the signs of hypoglycemia?": "'Sweating, confusion, shakiness' are common signs of hypoglycemia due to low blood sugar levels. Other options describe symptoms of dehydration or unrelated conditions.",
                    "What is the recommended daily fluid intake for adults?": "'2-3 liters' is the recommended daily fluid intake for adults to maintain hydration. Other options exceed or fall short of this range.",
                    "How do you prevent pressure ulcers?": "'Repositioning and skin care' are essential to prevent pressure ulcers by reducing prolonged pressure on the skin. Other options are unrelated to ulcer prevention.",
                    "What are the steps for administering an IV medication?": "'Prepare, verify, administer' ensures safe and accurate IV medication delivery. Other options mix unrelated procedures.",
                    "What is the normal heart rate range for children?": "'70-120 bpm' is the normal range for children, reflecting their higher metabolic rate compared to adults. Other options represent ranges for adults or extremes."
                }

                for i, q in enumerate(quiz_questions, start=1):
                    user_answer = user_answers.get(i)
                    is_correct = user_answer == q['answer']
                    total_marks += int(is_correct)
                    explanation = (
                        explanations[q['question']] if is_correct else
                        f"Incorrect. {explanations[q['question']]}"
                    )

                    results.append((q['question'], user_answer, explanation))

                st.success(f"Quiz submitted! You scored {total_marks} out of 10.")

                for i, (question, user_answer, explanation) in enumerate(results, start=1):
                    st.write(f"**Question {i}:** {question}")
                    st.write(f"Your answer: {user_answer}")
                    st.write(f"Explanation: {explanation}")
                    st.markdown("---")

                if st.button("Start New Quiz", key="new_quiz"):
                    previous_questions = set(q['question'] for q in st.session_state.quiz_questions)
                    new_questions = []

                    while len(new_questions) < 10:
                        candidate_questions = generate_mcq_questions()
                        for q in candidate_questions:
                            if q['question'] not in previous_questions and len(new_questions) < 10:
                                new_questions.append(q)
                                previous_questions.add(q['question'])

                    st.session_state.quiz_questions = new_questions  # Ensure new set of 10 questions
                    st.experimental_rerun()

if __name__ == "__main__":
    main()