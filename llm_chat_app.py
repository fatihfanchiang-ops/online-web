import streamlit as st
from openai import OpenAI

# 网页基础配置
st.set_page_config(page_title="简易LLM问答", page_icon="💬")
st.title("简易大语言模型问答界面")
st.divider()

# 初始化OpenAI客户端
# 请将 YOUR_API_KEY_HERE 替换为真实的 OpenAI API 密钥
client = OpenAI(api_key="YOUR_API_KEY_HERE")

# ===================== 方式1：文本输入框 + 提交按钮 =====================
st.subheader("方式1：文本输入 + 提交按钮")
user_question = st.text_input("请在这里输入你的问题：")
submit_btn = st.button("获取大模型回答")

# 判断：点击按钮，并且输入内容不为空
if submit_btn and user_question.strip() != "":
    with st.spinner("正在等待大模型回复..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_question}]
        )
        answer = response.choices[0].message.content
    st.write("**大模型回答：**")
    st.write(answer)

st.divider()

# ===================== 方式2：原生聊天气泡界面（推荐） =====================
st.subheader("方式2：聊天样式输入框")
chat_input = st.chat_input("输入问题进行提问...")

if chat_input:
    # 展示用户提问气泡
    st.chat_message("user").write(chat_input)
    with st.spinner("正在生成回答..."):
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": chat_input}]
        )
        llm_answer = resp.choices[0].message.content
    # 展示AI回答气泡
    st.chat_message("assistant").write(llm_answer)
