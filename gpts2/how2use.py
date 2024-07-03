import streamlit as st
from langchain_openai import OpenAI,ChatOpenAI
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from langchain.llms.fake import FakeListLLM
from start_sample import llmpage, logopage

st.set_page_config(
    page_title="HOW to Use GPT",
    page_icon="👋",
)

logopage()
# Streamlit 페이지에 제목 표시
st.markdown("### HOW 2 USE GPTs for EPC)PE Center! 👋")

st.markdown("# 👨‍🔧 GPT란?")
st.markdown("""
    #
    LLM
    Large Language Model
    말 잘하는 친구    
    #
            """)
st.markdown("---")
st.image(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\asset\how2use\image1.png")
st.markdown("""
    #
    보통 사람은 이럴 때 이런 말을 하지?
    라는 것을 확률화 하여 확률 대로 뱉어주기 때문에 결과가 랜덤함.
    주로 높은 확률인 것을 대답하지만, 0%에 가까운 것도 답변에 나오기도함.
    #
            """)
st.image(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\asset\how2use\image2.png")
st.image(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\asset\how2use\image3.png")
st.image(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\asset\how2use\image4.png")
st.markdown("---")
st.markdown("""
    #
    장점 : 말을 잘한다.
    단점 : 말만 잘한다.
    어떻게 써야하지?
    #
            """)
st.markdown("## 아무말이나 해도 되게 한다.")
st.markdown("""
    #
    - 요약 서비스 (유튜브나, 웹사이트에 있는 글들 요약) [Lilys AI](https://lilys.ai) 
    - 원어민급 영어회화 무료! [Youtube](https://www.youtube.com/watch?v=dKAy7iF7rHI) 
    - 개인정보와 카드의 말을 조합하여 타로운세 봐주는 서비스 [마이타로](https://www.aitimes.kr/news/articleView.html?idxno=27559)
        
    #""", unsafe_allow_html=True)

st.markdown("---")
st.image(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\asset\how2use\skimage1.png")

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