import streamlit as st
import os
from datetime import date
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
from langchain_openai import OpenAI,ChatOpenAI
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from langchain.llms.fake import FakeListLLM
import pymupdf4llm
import fitz

st.set_page_config(
    page_title="Upload RFP",
    page_icon="📚",
)
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

max_chars = 200000
label = 'multi_doc'+str(date.today())

# Function to write text to file
def write_to_library(segmented_text, file_name):
    folder_name = "files"
    file_folder_name = os.path.join(folder_name, file_name)
    if not os.path.exists(file_folder_name):
        os.makedirs(file_folder_name)
    path = os.path.join(file_folder_name, file_name + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(segmented_text)
    return path

# Function to parse uploaded file
def parse_file(user_file):
    file_type = user_file.type
    file_name = os.path.splitext(user_file.name)[0]
    with st.spinner("File is being processed..."):
        if file_type == "text/plain":
            all_text = str(user_file.read(), "utf-8", errors='ignore')
        elif file_type == "application/pdf":
            pdf_document = fitz.open(stream=user_file.read(), filetype="pdf")
            all_text = ""
            for page in pdf_document:
                all_text += page.get_text()
        else:
            st.error("Unsupported file type!")
            return None
    file_path_p = write_to_library(all_text, file_name)
    return file_path_p

# Function to call embedding script
def run_embedding_script(file_path):
    os.system(f"python embedding.py --file_path {file_path}")


if __name__ == '__main__':
    st.title("RFP Upload")
    st.markdown("**Upload documents**")
    
    uploaded_files = st.file_uploader("Choose .pdf/.word file", accept_multiple_files=True, type=["pdf", "txt"], key="a")
    file_path_list = []
    
    for uploaded_file in uploaded_files:
        file_path = parse_file(uploaded_file)
        file_path_list.append(file_path)
        run_embedding_script(file_path)
    
    if st.button("Remove file"):
        for file_path in file_path_list:
            if os.path.exists(file_path):
                os.remove(file_path)
                file_folder = os.path.dirname(file_path)
                if os.path.exists(file_folder):
                    os.rmdir(file_folder)
        st.write("Files removed successfully")
    
    st.text_input("PJT Name")
    st.markdown("**Admin will check PJT NAME and File after that it will inform to you**")
    st.button("Submit")
