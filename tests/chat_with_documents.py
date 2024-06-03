import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from gpt_servieces import llama_faiss_embedding, doc_reader
import streamlit as st

from langchain_community.vectorstores.faiss import FAISS
from langchain_community.llms.llamacpp import LlamaCpp

from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories.streamlit import StreamlitChatMessageHistory
from langchain_community.embeddings.llamacpp import LlamaCppEmbeddings

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter

llama_path=None
project_path=os.path.dirname(os.path.dirname(__file__))
drive_path = "llms"  # 사용자의 실제 하드 드라이브 경로로 수정해주세요.
model_basename = "ggml-model-Q4_K_M.gguf" # file name
destination_path = os.path.join(project_path,drive_path, model_basename)
llama_path=os.path.abspath(destination_path)
print(llama_path)
print(os.path.exists(llama_path))

st.set_page_config(page_title="LangChain: Chat with Documents", page_icon="🦜")
st.title("🦜 LangChain: Chat with Documents")


@st.cache_resource(ttl="1h")
@st.cache(allow_output_mutation=True, ttl=3600)
def configure_retriever(uploaded_files):
    if not uploaded_files:
        return None
    docs = []
    temp_dir = tempfile.TemporaryDirectory()

    for file in uploaded_files:
        temp_filepath = os.path.join(temp_dir.name, file.name)
        with open(temp_filepath, "wb") as f:
            f.write(file.getbuffer())  # file.getvalue() -> file.getbuffer()로 수정 필요
        faiss = llama_faiss_embedding.textfile2faiss(temp_filepath, resultpath=os.path.join(project_path, "temp", file.name),model_path=llama_path)
        if faiss is not None:
            docs.append(faiss)  # faiss가 None이 아닌 경우만 추가

    faissdbpaths = [doc for doc in docs if doc is not None]  # 유효한 경로만 포함

    if not faissdbpaths:
        return None  # 유효한 경로가 없으면 None 반환

    if len(faissdbpaths) > 1:
        result_location = llama_faiss_embedding.merge_faiss(faissdbpaths,model_path=llama_path)
        if os.path.exists(result_location):
            vectordb = llama_faiss_embedding.faiss2txt(resultpath=result_location,model_path=llama_path)
    elif len(faissdbpaths) == 1:
        vectordb = llama_faiss_embedding.faiss2txt(resultpath=faissdbpaths[0],model_path=llama_path)

    if vectordb:
        retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k": 4})
        return retriever
    return None


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)


class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.status = container.status("**Context Retrieval**")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        self.status.write(f"**Question:** {query}")
        self.status.update(label=f"**Context Retrieval:** {query}")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.status.write(f"**Document {idx} from {source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")


uploaded_files = st.sidebar.file_uploader(
    label="Upload PDF files", type=["pdf"], accept_multiple_files=True
)
if not uploaded_files:
    st.info("Please upload PDF documents to continue.")
    st.stop()

retriever = configure_retriever(uploaded_files)

# Setup memory for contextual conversation
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = ''
msgs = StreamlitChatMessageHistory(key="chat_history")
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

# Continue with setting up your LLM and QA chain as usual
llm = LlamaCpp(
    model_path=llama_path,
    n_batch=512,
    n_gpu_layers=-1,
    n_ctx=2056
)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm, retriever=retriever, memory=memory, verbose=True
)

if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    msgs.clear()
    msgs.add_ai_message("How can I help you?")

avatars = {"human": "user", "ai": "assistant"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me anything!"):
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())
        response = qa_chain.run(user_query, callbacks=[retrieval_handler, stream_handler])
