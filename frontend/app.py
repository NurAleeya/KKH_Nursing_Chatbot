import streamlit as st
from PIL import Image
import requests
import os
import json

def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_chat_history(chat_history, file_path):
    with open(file_path, "w") as file:
        json.dump(chat_history, file)

def delete_chat_history(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def rename_chat_history(file_path, new_name):
    if os.path.exists(file_path):
        dir_name = os.path.dirname(file_path)
        new_file_path = os.path.join(dir_name, new_name)
        os.rename(file_path, new_file_path)
        return new_file_path
    return None

def main():
    logo = Image.open("frontend/KKH_Logo.jpg")
    st.image(logo, width=100)  # Display the logo at the top of the page with a smaller width

    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='white-space: nowrap;'>KK Women's and Children's Hospital</h1>
        </div>
    """, unsafe_allow_html=True)
    st.subheader("Your 24/7 nurse assistant for clinical guidelines, calculations, and education.")

    st.sidebar.title("Select an option:")
    option = st.sidebar.radio("", ["Retrieve Clinical Guidelines", "Calculate Fluid Requirement", "Take a Quiz"])

    if option == "Retrieve Clinical Guidelines":
        st.header("Retrieve Clinical Guidelines")
        predefined_prompts = [
            "What are the steps for managing a cardiac arrest?",
            "How to assess a child's respiratory distress?",
            "What are the clinical guidelines for managing fever in children?",
            "How to calculate fluid requirements for pediatric patients?",
            "What are the steps for neonatal resuscitation?"
        ]
        selected_prompt = st.selectbox("Select a predefined prompt:", ["Select a prompt"] + predefined_prompts)
        query = st.text_area("Enter your query for clinical guidelines:", value=selected_prompt if selected_prompt != "Select a prompt" else "")

        chat_history_path = "c:/Users/23050830/KKH_Nursing_Chatbot_V2/data/chat_history.json"
        chat_history = load_chat_history(chat_history_path)

        # Implement caching for responses
        @st.cache_data
        def fetch_guidelines(query):
            try:
                payload = {
                    "model": "phi-2",
                    "messages": [{"role": "user", "content": query}],
                    "temperature": 0.7
                }
                response = requests.post("http://10.175.5.70:1234/v1/chat/completions", json=payload, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("choices", [{}])[0].get("message", {}).get("content", "No answer found.")
                    return answer.split(".")[0]  # Extract the first sentence for simplicity
                else:
                    return f"Failed to retrieve answer. Status code: {response.status_code}"
            except requests.exceptions.Timeout:
                return "The request timed out. Please try again later."
            except requests.exceptions.ConnectionError:
                return "Failed to connect to the server. Please check your network or server status."
            except Exception as e:
                return f"An error occurred: {e}"

        if st.button("Submit"):
            if query.strip():
                simplified_answer = fetch_guidelines(query)
                if "Failed" in simplified_answer or "error" in simplified_answer:
                    st.error(simplified_answer)
                else:
                    st.success(simplified_answer)

                    # Update chat history
                    chat_history.append({"user": query, "assistant": simplified_answer})
                    save_chat_history(chat_history, chat_history_path)
            else:
                st.warning("Please enter a valid query or select a predefined prompt.")

    elif option == "Calculate Fluid Requirement":
        st.header("Calculate Fluid Requirement")
        weight = st.number_input("Enter weight (kg):", min_value=0.0, step=0.1)
        if st.button("Calculate"):
            if weight > 0:
                try:
                    # Fluid requirement calculation based on standard formula
                    if weight <= 10:
                        fluid_requirement = weight * 100  # 100 ml/kg for first 10 kg
                    elif weight <= 20:
                        fluid_requirement = 1000 + (weight - 10) * 50  # 50 ml/kg for next 10 kg
                    else:
                        fluid_requirement = 1500 + (weight - 20) * 20  # 20 ml/kg for weight above 20 kg

                    st.info(f"Fluid requirement for {weight} kg: {fluid_requirement} ml/day")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter a valid weight greater than 0.")

    elif option == "Take a Quiz":
        st.header("Take a Quiz")
        st.write("Answer the following questions:")

        questions = [
            {
                "question": "What is the normal range for blood pressure?",
                "options": ["120/80 mmHg", "140/90 mmHg", "100/70 mmHg"],
                "correct": "120/80 mmHg",
                "explanation": "The normal range for blood pressure is 120/80 mmHg."
            },
            {
                "question": "What is the normal heart rate for adults?",
                "options": ["60-100 bpm", "40-60 bpm", "100-120 bpm"],
                "correct": "60-100 bpm",
                "explanation": "The normal heart rate for adults is 60-100 beats per minute."
            },
            {
                "question": "What is the normal respiratory rate for adults?",
                "options": ["12-20 breaths/min", "20-30 breaths/min", "10-15 breaths/min"],
                "correct": "12-20 breaths/min",
                "explanation": "The normal respiratory rate for adults is 12-20 breaths per minute."
            },
            {
                "question": "What is the normal temperature range for humans?",
                "options": ["36.5-37.5°C", "35.0-36.0°C", "37.5-38.5°C"],
                "correct": "36.5-37.5°C",
                "explanation": "The normal temperature range for humans is 36.5-37.5°C."
            },
            {
                "question": "What is the normal oxygen saturation level?",
                "options": ["95-100%", "90-95%", "85-90%"],
                "correct": "95-100%",
                "explanation": "The normal oxygen saturation level is 95-100%."
            },
            {
                "question": "What is the normal blood sugar level for fasting?",
                "options": ["70-100 mg/dL", "100-140 mg/dL", "50-70 mg/dL"],
                "correct": "70-100 mg/dL",
                "explanation": "The normal blood sugar level for fasting is 70-100 mg/dL."
            },
            {
                "question": "What is the normal cholesterol level?",
                "options": ["Below 200 mg/dL", "200-240 mg/dL", "Above 240 mg/dL"],
                "correct": "Below 200 mg/dL",
                "explanation": "The normal cholesterol level is below 200 mg/dL."
            }
        ]

        user_answers = []
        score = 0

        for idx, q in enumerate(questions):
            st.write(f"Question {idx + 1}: {q['question']}" )
            selected_option = st.radio(f"Select an answer for Question {idx + 1}", q['options'], key=f"q{idx}", index=None)
            user_answers.append((selected_option, q['correct'], q['explanation']))

        if st.button("Submit All Answers"):
            for idx, (selected_option, correct_answer, explanation) in enumerate(user_answers):
                st.write(f"Question {idx + 1}: {questions[idx]['question']}" )
                if selected_option == correct_answer:
                    st.success(f"Correct! The normal {questions[idx]['question'].split(' ')[-2]} is {correct_answer}. {explanation}")
                    score += 1
                else:
                    st.error(f"Incorrect. The correct answer is {correct_answer} because {explanation}")

            st.write(f"Your total score: {score}/{len(questions)}")

if __name__ == "__main__":
    main()
