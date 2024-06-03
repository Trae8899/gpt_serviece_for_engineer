import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

st.set_page_config(
    page_title="Engineering GPTs",
    page_icon="👋",
)
add_page_title()

show_pages(
    [
        Page(r"gpts\page.py", "Engineering GPTs", "💻", in_section=False),
        Page(r"gpts\page2_embedding.py", "HOW to Use GPT", "💻", in_section=False),
        
        # GPT 사용법
        Section("Engineering GPTs", "👨‍🔧"),
        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\page2\Week_2_Workflow_Orchestration.py", "LL Search", "📚", in_section=True),
        Page(r"gpts\page3_engineering_chatbot.py", "Engineering Chatbot", "1️⃣", in_section=True),
        
        Section("RFP Search Tool", "👨‍🔧"),
        Page(r"gpts\page3_embedding.py",  "Upload RFP", "📚", in_section=True),
        Page(r"gpts\excelshow.py", "Check Toxic Clause", "1️⃣", in_section=True),
        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\gpts\RAG_Feedback.py", "Chat for Client Comment", "❔", in_section=True),
        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\gpts\RAG_Feedback.py", "Just Chatbot", "❔", in_section=True),

        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\page2\Week_7_Project.py", "FAQ", "❔", in_section=False),
    ]
)
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
    st.session_state['llms'] = st.session_state.selectbox

# 사이드바에서 모듈 선택
selectbox = st.sidebar.selectbox(
    "Which Module do you want?",
    ("OPENAI", "AZURE OPEN AI", "FAKELLM"),
    index=["OPENAI", "AZURE OPEN AI", "FAKELLM"].index(st.session_state['llms']),
    key='selectbox',
    on_change=update_llms
)

if st.session_state['llms'] == "OPENAI":
    st.session_state['OPENAIAPI'] = st.sidebar.text_input("API KEY", value=st.session_state['OPENAIAPI'])
elif st.session_state['llms'] == "AZURE OPEN AI":
    st.session_state['AZURE_OPENAI_API_KEY'] = st.sidebar.text_input("API KEY", value=st.session_state['AZURE_OPENAI_API_KEY'])
    st.session_state['AZURE_OPENAI_ENDPOINT'] = st.sidebar.text_input("END POINT", value=st.session_state['AZURE_OPENAI_ENDPOINT'])


# Streamlit 페이지에 제목 표시
st.write("# Welcome to GPT Service by J.Park! 👋")
hide_pages(["Thank you"])

st.markdown("### 👨‍🔧 GPTs Service by [JH.Park](https://github.com/Trae8899)")

st.image(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\icon\Doosan_Logo.jpg")

st.info("Original Course Repository on [Github](https://github.com/Trae8899/gpt-docs-chatbot-python-flet)")

st.markdown("---")

with st.expander("Contact with Me"):
    st.markdown("""
    
    <a href="qkrwogus88@naver.com"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>

    #
    - Join the [KAKAO TALK](https://open.kakao.com/o/gu9Qe3pg) password : 1516
    - The videos are published on [News for All About](https://www.youtube.com/@monews8899) in
    - [LINKED IN](https://www.linkedin.com/in/jaehyun-park88/)
        
    #""", unsafe_allow_html=True)

st.markdown("""### 🔎 Overview""")
st.image("https://github.com/Trae8899/chatbot-Faiss/blob/main/Concept.png")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 