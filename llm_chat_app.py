import streamlit as st
from groq import Groq

# 填入 console.groq.com 获取的 API Key
GROQ_API_KEY = "在此贴上你的key"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="简易LLM问答", page_icon="💬")
st.title("简易大语言模型问答界面")
st.divider()

def get_ai_response(question):
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": question}],
        temperature=0.7
    )
    return completion.choices[0].message.content

# 方式1：文本输入框 + 提交按钮
st.subheader("方式1：文本输入 + 提交按钮")
user_question = st.text_input("请在这里输入你的问题：")
submit_btn = st.button("获取大模型回答")

if submit_btn and user_question.strip() != "":
    with st.spinner("正在等待大模型回复..."):
        answer = get_ai_response(user_question)
    st.write("**大模型回答：**")
    st.write(answer)

st.divider()

# 方式2：聊天气泡界面
st.subheader("方式2：聊天样式输入框")
chat_input = st.chat_input("输入问题进行提问...")

if chat_input:
    st.chat_message("user").write(chat_input)
    with st.spinner("正在生成回答..."):
        llm_answer = get_ai_response(chat_input)
    st.chat_message("assistant").write(llm_answer)
