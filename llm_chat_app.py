import streamlit as st
from groq import Groq

# Read API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# Page config
st.set_page_config(page_title="Simple LLM Chat App", page_icon="🤖")
st.title("Simple LLM Chat Interface")
st.divider()

# -------- Part12: Privacy & Safety Notice --------
with st.expander("⚠️ Important Safety Notice", expanded=False):
    st.markdown("""
- Large‑language models may produce incorrect or hallucinated answers.
- **Do NOT input passwords, ID numbers, private address or any sensitive personal information.**
- This chat is for educational use only.
""")

# -------- Part10: Two user selectable options --------
st.subheader("Settings for Python Tutor")
difficulty_level = st.selectbox(
    "Select Python difficulty level",
    ["Beginner", "Intermediate", "Advanced"]
)
response_format = st.radio(
    "Choose output format",
    ["Paragraph text", "Bullet‑point list"]
)

# Build system prompt Part9: Assign AI role (Python tutor)
system_prompt = f"""
You are a helpful Python programming tutor.
Difficulty level: {difficulty_level}
Output format requirement: {response_format}
Only answer questions related to Python programming.
If user asks something unrelated to Python, politely refuse to answer and tell user to ask Python‑related questions.
Give clear, accurate answers.
"""

# Function Part9 + Part11 Exception handling
def get_ai_response(user_question: str, system_text: str):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content

    except Exception as err:
        st.error(f"API Connection Error: {str(err)}")
        return "⚠️ Failed to get reply from LLM. Please check your API key, network or quota limit."


st.divider()
# Mode1: Text input + submit button
st.subheader("Mode 1: Text input with submit button")
user_question = st.text_input("Please enter your Python question here:")
submit_btn = st.button("Get LLM answer")

if submit_btn:
    if not user_question.strip():
        st.warning("Please input a valid question!")
    else:
        with st.spinner("Waiting for LLM response ..."):
            ai_reply = get_ai_response(user_question, system_prompt)
            st.markdown("**LLM Answer:**")
            st.write(ai_reply)

st.divider()
# Mode2: Native chat bubble interface
st.subheader("Mode 2: Chat‑bubble input box")
chat_input_text = st.chat_input("Ask your Python question ...")

if chat_input_text:
    if not chat_input_text.strip():
        st.warning("Empty question, please type content.")
    else:
        st.chat_message("user").write(chat_input_text)
        with st.spinner("Generating answer ..."):
            llm_result = get_ai_response(chat_input_text, system_prompt)
            st.chat_message("assistant").write(llm_result)
