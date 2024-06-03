import openai
import streamlit as st
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI

st.set_page_config(page_title="RAG : Simple Feedback", page_icon="🦜")
st.title("🦜 RAG : Simple Feedback")

# openai_api_key = st.secrets.get("OPENAI_API_KEY")
openai_api_key=None
if not openai_api_key:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.warning("Please add an OpenAI API Key to continue")
    st.stop()

# LangChain 설정
llm = OpenAI(openai_api_key=openai_api_key)
memory = ConversationBufferMemory()
llm_chain = ConversationChain(llm=llm, memory=memory)

# 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 초기화
reset_history = st.sidebar.button("Reset chat history")
if reset_history:
    st.session_state.messages = []
    st.session_state.last_response = None

# 채팅 기록 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if input := st.chat_input(placeholder="Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": input})
    st.chat_message("user").write(input)

    # LangChain을 사용한 OpenAI API 호출
    response = llm_chain.run(input)
    
    # 응답 저장 및 표시
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# 피드백 섹션
# feedback = st.radio("How was the response?", ("😀", "🙂", "😐", "🙁", "😞"))
scores = {"Good": 1, "Not Bad": 0.75, "Soso": 0.5, "Bad": 0.25, "Terrible": 0}
feedback = st.radio("How was the response?", ("Good", "Not Bad", "Soso", "Bad", "Terrible"))
if st.button("Submit Feedback"):
    st.write("Feedback recorded! Thank you.")
