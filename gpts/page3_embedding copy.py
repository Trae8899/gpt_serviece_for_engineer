import streamlit as st
import re
from icon.pageset import apply_studio_style
import os
from datetime import date

from st_pages import Page, Section, show_pages, add_page_title, hide_pages

st.set_page_config(
    page_title="Engineering GPTs",
    page_icon="👋",
)
add_page_title()

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

max_chars = 200000
label = 'multi_doc'+str(date.today())


def write_to_library(segmented_text, file_name):
    folder_name = "file"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    path = f"./{folder_name}/{file_name}.txt"
    f = open(path, "w")
    f.write(segmented_text)
    f.close()

    return path


def parse_file(user_file):
    file_type = user_file.type
    with st.spinner("File is being processed..."):
        if file_type == "text/plain":
            all_text = str(user_file.read(), "utf-8", errors='ignore')
        else:
            with pdfplumber.open(user_file) as pdf:
                all_text = [p.extract_text() for p in pdf.pages][0]

    file_path_p = write_to_library(all_text, user_file.name)
    return file_path_p
        

def upload_file(file_path_p):
    try:
        file_id_p = client.library.files.create(file_path=file_path_p, labels=label)
        st.session_state['files_ids'] = file_id_p
        st.session_state['file_uploaded'] = True
    except UnprocessableEntity:
        file_id_p = None
    return file_id_p


st.set_page_config(page_title="Multi-Document Q&A")

if __name__ == '__main__':
    apply_studio_style()
    st.title("Multi-Document Q&A")
    st.markdown("**Upload documents**")
    
    uploaded_files = st.file_uploader("choose .pdf/.txt file ",
                                      accept_multiple_files=True,
                                      type=["pdf", "text", "txt"],
                                      key="a")
    file_id_list = list()
    file_path_list = list()
    for uploaded_file in uploaded_files:
        file_path = parse_file(uploaded_file)
        file_id = upload_file(file_path)
        file_id_list.append(file_id)
        file_path_list.append(file_path)

    if st.button("Remove file"):
        for file in file_path_list:
            try:
                os.remove(file)
            except UnprocessableEntity:
                pass
        try:
            client.library.files.delete(st.session_state['files_ids'])
        except UnprocessableEntity:
            pass
        # for file in file_id_list:
        #     with st.spinner("Loading..."):
        #         try:
        #             client.library.files.delete(file)
        #         except:
        #             continue

        st.write("files removed successfully")

    st.markdown("**Ask a question about the uploaded document, and here is the answer:**")

    question = st.chat_input("What would you like to know?")
    if question:
        response = client.library.answer.create(question=question, label=label)
        if response.answer is None:
            st.write("The answer is not in the documents")
        else:
            st.write(response.answer)
        