# AI Python Tutor - LLM Web Application

## Project Name
**AI Python Tutor**

## Purpose
This web application acts as a beginner-friendly Python programming tutor. It helps students ask questions about Python concepts and receives clear, structured explanations from a Large Language Model (LLM) through an API connection.

## Web Tool
**Streamlit** (Python web framework)

Streamlit provides the web interface: text input area, submit button, select boxes for user options, loading spinner, and the response display area.

## LLM Provider
**Groq**

Groq offers a free tier suitable for educational projects. It requires an account and an API key, and provides fast inference for open-source models.

## Model Used
**llama-3.1-8b-instant** (Meta Llama 3.1, served by Groq)

- **Provider:** Meta (model), Groq (API hosting)
- **Main purpose:** General-purpose chat and instruction following
- **Free access:** Yes, under Groq free tier
- **Limitations:** Rate limits and token limits apply on the free tier

## Connection - How It Works
1. The user types a Python question in the Streamlit web interface.
2. The user selects two options: **Difficulty Level** and **Response Format**.
3. The Python application builds a request containing:
   - A **system instruction** that defines the AI's role (Python tutor) and incorporates the user's selected options.
   - The **user message** (the question typed in the text area).
4. The application sends this request to the **Groq API endpoint** using the Groq Python SDK, authenticated with the **API key**.
5. The Groq server forwards the request to the **llama-3.1-8b-instant** model.
6. The model generates a response and returns it as a **JSON response**.
7. The Python application extracts the text content from the JSON response.
8. Streamlit displays the response back to the user in the web browser.

**Flow:**
`User → Web Browser (Streamlit UI) → Python Application → Groq API → LLM (llama-3.1-8b-instant) → API JSON Response → Python Application → Web Browser → User`

## API Key Security
- The API key is **never hard-coded** in the source code.
- For local development, the key is stored in a `.env` file (loaded via `python-dotenv`), and `.env` is added to `.gitignore` so it is never pushed to GitHub.
- For Streamlit Cloud deployment, the key is stored in **Streamlit Secrets** (`st.secrets["GROQ_API_KEY"]`).
- The repository contains no API key in any file.

## User Options (Part 10)
The application provides two user-controlled options that affect the LLM response:
1. **Difficulty Level:** Beginner / Intermediate / Advanced
2. **Response Format:** Short Paragraph / Bullet Points

Both options are inserted into the system instruction so the model adapts its answer accordingly.

## Error Handling (Part 11)
The application handles the following problems with user-friendly messages:
- Empty user input (shows a warning, does not send the request)
- Invalid or missing API key
- Free API rate limit reached
- Request timeout
- Model unavailable
- General API / network connection errors

All errors are caught with `try/except` and displayed using `st.error()`, so the application never crashes.

## Limitations
- The free Groq tier has rate limits; heavy use may be temporarily blocked.
- The AI may produce incorrect code or explanations — users should verify important information.
- The tutor only handles Python-related questions; off-topic questions are politely declined.
- Responses are not saved between sessions (no conversation history / memory).

## References / Official Documentation
- Groq API Documentation: https://console.groq.com/docs
- Groq Python SDK: https://github.com/groq/groq-python
- Streamlit Documentation: https://docs.streamlit.io/
- Streamlit Secrets: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
