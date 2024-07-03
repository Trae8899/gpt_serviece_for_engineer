import streamlit as st
from langchain_openai import OpenAI,ChatOpenAI
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from langchain.llms.fake import FakeListLLM

def basepage():

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
