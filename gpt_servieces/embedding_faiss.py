import dotenv 
import openai
# PDF Loaders. If unstructured gives you a hard time, try PyPDFLoader
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import pymupdf4llm


MODEL = "text-embedding-ada-002"
OPENAI_API_KEY = None
try:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
except:
    pass


def openai_pdf2faiss(filepath:str,openai_api_key=OPENAI_API_KEY,resultpath=None): 
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key)
    md_text=pymupdf4llm.to_markdown(filepath,write_images=True,)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    text = text_splitter.split_documents(md_text)
    faissdb = FAISS.from_documents(text, embeddings)
    resultfilepath=os.path.join(resultpath,os.path.basename(filepath))
    if os.path.exists(resultfilepath):
        pass
    else:
        pass
    faissdb.save_local(resultfilepath)
    return resultfilepath

def textfile2faiss(filepath:str,openai_api=OPENAI_API_KEY,resultpath=None)->str: 
    if resultpath==None or resultpath=='':
        resultpath=os.path.dirname(filepath)
    if os.path.exists(resultpath):
        pass
    else:
        return
    embeddings=OpenAIEmbeddings(openai_api_key=openai_api)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    
    basename = os.path.basename(filepath)
    filenames=os.path.splitext(basename)
    ext=filenames[1]
    filename=filenames[0]
    if ext.upper()==".PDF":
        loader = PyPDFLoader(filepath)
    elif ext.upper()==".DOCX":
        loader = Docx2txtLoader(filepath)
    else:
        return
    document = loader.load()
    text = text_splitter.split_documents(document)
    faissdb = FAISS.from_documents(text, embeddings)
    resultfilepath=os.path.join(resultpath,f"{filename}_index")
    if os.path.exists(resultfilepath):
        pass
    else:
        pass
    faissdb.save_local(resultfilepath)
    return filename