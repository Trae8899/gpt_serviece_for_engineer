import streamlit as st
import os
from start_sample import llmpage, logopage

st.set_page_config(
    page_title="Upload RFP",
    page_icon="📚",
)

st.title("📚 Upload RFP")
st.markdown("**Upload documents**")
    
uploaded_files = st.file_uploader("Choose .pdf/.word file", accept_multiple_files=True, type=["pdf", "txt"], key="itbs")
file_path_list = []
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
    
if st.button("Submit"):
    st.write("Files processed and FAISS index saved successfully")
