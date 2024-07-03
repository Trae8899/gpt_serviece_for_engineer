import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
from langchain_openai import OpenAI,ChatOpenAI
from langchain_openai import AzureOpenAI,AzureChatOpenAI
from langchain.llms.fake import FakeListLLM
from start_sample import basepage as bsp

st.set_page_config(
    page_title="Engineering GPTs",
    page_icon="👋",
)

bsp()

