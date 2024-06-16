import streamlit as st
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI,ChatOpenAI
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from langchain.llms.fake import FakeListLLM
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
from streamlit_feedback import streamlit_feedback

st.set_page_config(page_title="RFP Search Bot", page_icon="🦜")
st.title("🦜 RFP Search Bot")
st.sidebar.image(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\asset\Doosan_Logo.jpg")
st.sidebar.write("# EPC)PE CENTER 👋")

st.sidebar.success("Select a model that you want.")

if 'llms' not in st.session_state:
    st.session_state['llms'] = 'OPENAI'
if 'OPENAIAPI' not in st.session_state:
    st.session_state['OPENAIAPI'] = None
if 'AZURE_OPENAI_API_KEY' not in st.session_state:
    st.session_state['AZURE_OPENAI_API_KEY'] = None
if 'AZURE_OPENAI_ENDPOINT' not in st.session_state:
    st.session_state['AZURE_OPENAI_ENDPOINT'] = None

# 사이드바에서 모듈 선택
def update_llms():
    st.session_state['llms'] = st.session_state.selectllm

# 사이드바에서 모듈 선택
selectllm = st.sidebar.selectbox(
    "Which Module do you want?",
    ("OPENAI", "AZURE OPEN AI", "FAKELLM"),
    index=["OPENAI", "AZURE OPEN AI", "FAKELLM"].index(st.session_state['llms']),
    key='selectllm',
    on_change=update_llms
)

if st.session_state['llms'] == "OPENAI":
    st.session_state['OPENAIAPI'] = st.sidebar.text_input("API KEY", value=st.session_state['OPENAIAPI'],type="password")
    llm = ChatOpenAI(openai_api_key=st.session_state['OPENAIAPI'],model="gpt-4o")
    
elif st.session_state['llms'] == "AZURE OPEN AI":
    st.session_state['AZURE_OPENAI_API_KEY'] = st.sidebar.text_input("API KEY", value=st.session_state['AZURE_OPENAI_API_KEY'])
    st.session_state['AZURE_OPENAI_ENDPOINT'] = st.sidebar.text_input("END POINT", value=st.session_state['AZURE_OPENAI_ENDPOINT'])
    llm = AzureChatOpenAI()
else:
    llm=FakeListLLM(responses=["fakellm1","fakellm2","fakellm3"])


# LangChain 설정
pjtname=st.selectbox(
    "PJT NAME",
    ("jawa9&10","lumar","samcheok"),
    )
# gpt-3.5-turbo-instruct
# llm = ChatOpenAI(openai_api_key=st.session_state['OPENAIAPI'],model="gpt-4o")
# llm = OpenAI(openai_api_key=st.session_state['OPENAIAPI'],model_name="gpt-4o")
memory = ConversationBufferMemory()
llm_chain = ConversationChain(llm=llm, memory=memory)



# 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.feedback_scores = []

# 채팅 기록 초기화
reset_history = st.sidebar.button("Reset chat history")
if reset_history:
    st.session_state.messages = []
    st.session_state.feedback_scores = []
    st.session_state.last_response = None

# 채팅 기록 표시
for i, msg in enumerate(st.session_state.messages):
    st.chat_message(msg["role"]).write(msg["content"])
    if msg["role"] == "assistant":
        feedback = streamlit_feedback(
            feedback_type="faces",
            optional_text_label="[Optional] Please provide an explanation",
            key=f"feedback_{i}",
        )
        if feedback:
            scores = {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0}
            score = scores[feedback["score"]]
            st.session_state.feedback_scores.append({"index": i, "score": score, "comment": feedback.get("text", "")})
            if feedback.get("text"):
                st.write(f"Comment: {feedback['text']}")

# 사용자 입력 처리
if input := st.chat_input(placeholder="Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": input})
    st.chat_message("user").write(input)

    # LangChain을 사용한 OpenAI API 호출
    response = llm_chain.run(input)
    
    # 응답 저장 및 표시
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

    with st.expander("Show Original Lessons"):
        st.write("원본 retriever data 몇개")

# 피드백을 반영한 다음 대화 조정
def adjust_response_based_on_feedback(response, feedback_scores):
    if not feedback_scores:
        return response

    # 가장 최근의 피드백을 사용하여 조정
    latest_feedback = feedback_scores[-1]
    score = latest_feedback["score"]
    
    if score < 0.5:
        return "I'm sorry if my previous responses were not helpful. How can I assist you better?"
    elif score < 0.75:
        return "I'll try to improve my responses. What else would you like to know?"
    else:
        return response

# 마지막 응답에 대한 피드백을 반영한 후속 질문
if st.session_state.messages and st.session_state.feedback_scores:
    last_response = st.session_state.messages[-1]["content"]
    adjusted_response = adjust_response_based_on_feedback(last_response, st.session_state.feedback_scores)
    if adjusted_response != last_response:
        st.write(f"Adjusted response: {adjusted_response}")