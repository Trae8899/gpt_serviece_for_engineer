from pathlib import Path

import streamlit as st

from langchain.agents import AgentExecutor, Tool
from langchain.agents import create_react_agent

from langchain.chains.llm_math.base import LLMMathChain
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from langchain.chains.sql_database import query

from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from langchain_core.runnables import RunnableConfig
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.llamacpp import LlamaCppEmbeddings

from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAI
from langchain_community.llms.llamacpp import LlamaCpp

import sqlite3

from streamlit_agent.callbacks.capturing_callback_handler import playback_callbacks
from streamlit_agent.clear_results import with_clear_container

import os
import dotenv
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
OPENAI_API_KEY = None


DB_PATH = (r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\streamlit_agent\Chinook.db")
FAISS_INDEX_PATH=r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\faiss_index"

SAVED_SESSIONS = {
    "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?": "leo.pickle",
    "What is the full name of the female artist who recently released an album called "
    "'The Storm Before the Calm' and are they in the FooBar database? If so, what albums of theirs "
    "are in the FooBar database?": "alanis.pickle",
}

st.set_page_config(
    page_title="JH ENGINEERING GPT", page_icon="🆘", layout="wide", initial_sidebar_state="collapsed"
)
"# 🦜🔗 chatbot"

# Setup credentials in Streamlit

user_llms=st.sidebar.selectbox("Select Models",{"OPENAI","AOAI","Llama"})
user_openai_api_key=None
llama_path=None
project_path=os.path.dirname(os.path.dirname(__file__))
drive_path = "llms"  # 사용자의 실제 하드 드라이브 경로로 수정해주세요.
model_basename = "ggml-model-Q4_K_M.gguf" # file name
destination_path = os.path.join(project_path,drive_path, model_basename)
llama_path=destination_path
if user_llms=="OPENAI":
    user_openai_api_key = st.sidebar.text_input(
        "OpenAI API Key", type="password", help="Set this to run your own custom questions."
    )
    if user_openai_api_key=='':
        enable_custom = False
        try:
            OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
            user_openai_api_key=OPENAI_API_KEY
            enable_custom = True
        except:
            pass
elif user_llms=="AOAI":
    print(llama_path)
    print(os.path.exists(llama_path))
    enable_custom = True

# Tools setup
llm_openai = OpenAI(temperature=0, openai_api_key=user_openai_api_key, streaming=True)
llm_llama= LlamaCpp(
    temperature=0,
    model_path=llama_path,
    n_threads=2, # CPU cores
    n_batch=512, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    n_gpu_layers=-1, # Change this value based on your model and your GPU VRAM pool.
    n_ctx=1024, # Context window)
)
if user_llms=="OPENAI":
    llm=llm_openai
    embd = OpenAIEmbeddings(model="text-embedding-3-small", disallowed_special=())
elif user_llms=="Llama":
    llm=llm_llama
    embd = LlamaCppEmbeddings(model_path=llama_path)
search = DuckDuckGoSearchAPIWrapper()

llm_math_chain = LLMMathChain.from_llm(llm)
from langchain.tools.retriever import create_retriever_tool
# embeddings 인스턴스를 생성합니다.
embd = OpenAIEmbeddings(model="text-embedding-3-small", disallowed_special=())

# embeddd = OpenAIEmbeddings(model="text-embedding-ada-002")
store = LocalFileStore("./cache/")
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
    embd, store, namespace=embd.model
)
vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embd,allow_dangerous_deserialization=True)

# retriever 생성
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":4})

retrivertool = create_retriever_tool(
    retriever,
    name="ASME/AWWA Chatbot",
    description = "useful for when you need to answer questions about ASME/AWWA Code. and it is used for engineering field. Input should be in the form of a question containing full context",
)

# Make the DB connection read-only to reduce risk of injection attacks
# See: https://python.langchain.com/docs/security
creator = lambda: sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
db = SQLDatabase(create_engine("sqlite:///", creator=creator))
db_chain = query.create_sql_query_chain(llm, db)
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
    ),
    Tool(
        name="FooBar DB",
        func=db_chain.invoke,
        description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context",
    ),
    retrivertool
]

# Initialize agent
prompt_text=UnstructuredMarkdownLoader(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\instruction\tools_arrangement.md").load()
react_agent = create_react_agent(llm, tools, prompt=PromptTemplate.from_template(prompt_text[0].page_content))
mrkl = AgentExecutor(agent=react_agent, tools=tools)

with st.form(key="form"):
    if not enable_custom:
        "Ask one of the sample questions, or enter your API Key in the sidebar to ask your own custom questions."
    prefilled = st.selectbox("Sample questions", sorted(SAVED_SESSIONS.keys())) or ""
    user_input = ""

    if enable_custom:
        user_input = st.text_input("Or, ask your own question")
    if not user_input:
        user_input = prefilled
    submit_clicked = st.form_submit_button("Submit Question")

output_container = st.empty()
if with_clear_container(submit_clicked):
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)

    answer_container = output_container.chat_message("assistant", avatar="🦜")
    st_callback = StreamlitCallbackHandler(answer_container)
    cfg = RunnableConfig()
    cfg["callbacks"] = [st_callback]

    # If we've saved this question, play it back instead of actually running LangChain
    # (so that we don't exhaust our API calls unnecessarily)
    if user_input in SAVED_SESSIONS:
        session_name = SAVED_SESSIONS[user_input]
        session_path = Path(__file__).parent / "runs" / session_name
        print(f"Playing saved session: {session_path}")
        answer = playback_callbacks([st_callback], str(session_path), max_pause_time=2)
    else:
        answer = mrkl.invoke({"input": user_input}, cfg)

    answer_container.write(answer["output"])
