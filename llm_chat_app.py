"""
AI Python Tutor - LLM Web Application
Built with Streamlit + Groq API
"""

import streamlit as st
from groq import Groq

# -----------------------------
# API Client Setup
# API key is stored in Streamlit Secrets (never hard-coded)
# -----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="AI Python Tutor", page_icon="🐍", layout="centered")

st.title("🐍 AI Python Tutor")
st.markdown("A web application that helps beginners learn Python programming, powered by a Large Language Model.")

# -----------------------------
# Part 12 - User Privacy & Safety Notice
# -----------------------------
with st.expander("⚠️ Important Notice - Please Read", expanded=True):
    st.markdown("""
    - AI responses **may contain mistakes**. Always verify important information.
    - Do **NOT** enter passwords, home addresses, ID numbers, or any private / sensitive personal information.
    - This tutor is for Python learning only.
    """)

st.divider()

# -----------------------------
# Part 10 - Two User-Controlled Options
# -----------------------------
st.subheader("Customize Your Answer")

col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox(
        "Difficulty Level",
        ["Beginner", "Intermediate", "Advanced"],
        help="Controls how advanced the explanation will be."
    )

with col2:
    output_style = st.radio(
        "Response Format",
        ["Short Paragraph", "Bullet Points"],
        help="Controls how the answer is structured."
    )

st.divider()

# -----------------------------
# Part 9 - Custom System Instruction
# The AI has a specific role: beginner-friendly Python tutor.
# -----------------------------
def build_system_prompt(diff, style):
    return f"""You are a friendly, patient Python programming tutor for students.

Your role:
- Help users understand Python concepts clearly.
- Use simple language and short code examples when helpful.
- Stay focused on Python programming. If the user asks an unrelated topic, politely remind them you are a Python tutor.

User-selected options (you MUST follow these):
- Difficulty level: {diff}
- Response format: {style}

If the format is "Bullet Points", answer using a markdown bullet list.
If the format is "Short Paragraph", answer in 2-4 concise paragraphs.
"""

# -----------------------------
# Part 7 / Part 11 - LLM Connection with Error Handling
# -----------------------------
def get_ai_response(question, system_text):
    """Send one user message to the LLM and return the response text.
    Handles common API failures gracefully.
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_text},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content

    except Exception as e:
        error_msg = str(e).lower()
        if "api key" in error_msg or "authentication" in error_msg or "401" in error_msg:
            return "ERROR: Invalid or missing API key. Please check the API key configuration."
        elif "rate limit" in error_msg or "429" in error_msg:
            return "ERROR: Free API usage limit reached. Please wait a moment and try again."
        elif "timeout" in error_msg:
            return "ERROR: Request timed out. Please check your internet connection and try again."
        elif "model" in error_msg:
            return "ERROR: The selected model is currently unavailable. Please try again later."
        else:
            return f"ERROR: Something went wrong while connecting to the AI service. Details: {str(e)}"

# -----------------------------
# Part 8 - Web Interface: Input + Submit + Response
# -----------------------------
st.subheader("Ask Your Python Question")

question = st.text_area(
    "Type your question here:",
    placeholder="e.g. What is a for loop in Python?",
    height=120
)

ask_button = st.button("Ask AI Tutor", type="primary")

if ask_button:
    # Part 11 - Empty input handling
    if not question.strip():
        st.error("Please enter a question first. Empty input is not allowed.")
    else:
        system_prompt = build_system_prompt(difficulty, output_style)
        with st.spinner("Thinking... Please wait for the AI response."):
            answer = get_ai_response(question, system_prompt)

        if answer.startswith("ERROR"):
            st.error(answer)
        else:
            st.success("Here is your answer:")
            st.markdown("### 🤖 AI Tutor Response")
            st.write(answer)

st.divider()
st.caption("Built with Streamlit · LLM Provider: Groq · Model: llama-3.1-8b-instant")
