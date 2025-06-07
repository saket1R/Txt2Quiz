import streamlit as st
import requests

st.set_page_config(page_title="Text2Quiz Generator", layout="wide")

st.title(" Text2Quiz Generator  ( SAVES YOUR MONEY FROM USELESS TEST SERIES )")

# --- User API Key ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]


# --- User Input ---
option = st.radio(
    "Choose input method:",
    ("Upload a .txt file", "Enter custom text manually")
)

content = ""

if option == "Upload a .txt file":
    uploaded_file = st.file_uploader(" Upload your .txt file here", type=["txt"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")

elif option == "Enter custom text manually":
    user_prompt = st.text_area(" Enter your topic/content below")
    if user_prompt.strip():
        content = user_prompt


# --- Function to generate quiz ---
def generate_quiz(prompt_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "You are a quiz generator for academic subjects like JEE."
            },
            {
                "role": "user",
                "content": f"""Generate 5 multiple-choice questions from the following content.
Each question should have 4 options (A to D) and indicate the correct answer.
Keep it simple and JEE-level standard.

Content:
\"\"\"
{prompt_text}
\"\"\""""
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Trigger button ---
if st.button(" Generate Quiz"):
    if not GROQ_API_KEY:
        st.error("❗ Please enter a valid Groq API key.")
    elif not content:
        st.warning(" Please upload a file or enter text.")
    else:
        with st.spinner(" Generating quiz..."):
            quiz = generate_quiz(content)
            st.success(" Quiz generated successfully!")
            st.markdown(" Quiz Output")
            st.code(quiz)


# --- Footer ---
st.markdown("---")
st.markdown("Made with using [LLaMA 3.1-8B Instant via Groq](https://console.groq.com)")