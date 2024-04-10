import dotenv 

from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from openai import AzureOpenAI
import openai
from langchain.vectorstores.faiss import FAISS
from gpt_servieces.doc_reader import textfile_reader
import datetime

MODEL = "text-embedding-3-small"
OPENAI_API_KEY = None
try:
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
except:
    pass

store = LocalFileStore("./cache/")
# embeddings 인스턴스를 생성합니다.
embd = OpenAIEmbeddings(model="text-embedding-3-small", disallowed_special=())

cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
    embd, store, namespace=embd.model
)

def textfile2faiss(filepath:str,chunk_size_set=1000,overlap_set=100,model="OPENAI",api_key=OPENAI_API_KEY,resultpath=None)->str: 
    if resultpath==None or resultpath=='':
        resultpath=os.path.dirname(filepath)
    if os.path.exists(resultpath):
        pass
    else:
        return
    
    embeddings=OpenAIEmbeddings(openai_api_key=api_key)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size_set, chunk_overlap=overlap_set)

    txt=textfile_reader(filepath)
    text = text_splitter.split_text(txt)
    faissdb = FAISS.from_documents(text, embeddings)
    
    basename = os.path.basename(filepath)
    filenames=os.path.splitext(basename)
    filename=filenames[0]

    resultfilepath=os.path.join(resultpath,f"{filename}_index")
    if os.path.exists(resultfilepath):
        pass
    else:
        pass
    faissdb.save_local(resultfilepath)
    return filename

def merge_faiss(faissfolderpaths,model="OPENAI",api_key=OPENAI_API_KEY,resultpath=None,name=None):
    embeddings=OpenAIEmbeddings(openai_api_key=api_key)
    
    if name==None:
        name="faiss_index"
    if resultpath==None:
        resultpath=os.path.dirname(faissfolderpaths[0])

    faissdbs=[]
    faissdbspath=[]
    for faisspath in faissfolderpaths:
        try:
            faissdb = FAISS.load_local(faisspath,embeddings=embeddings)
            faissdbs.append(faissdb)
            faissdbspath.append(faisspath)
        except Exception as err:
            print (err)
            continue

    faissdb_index=None
    faissdb_index = faissdbs[0]
    for faissdb in faissdbs[1:]:
        try:
            faissdb_index.merge_from(faissdb)
        except:
            continue
    
    result_faiss_path = os.path.join(resultpath,name)
    os.makedirs(result_faiss_path, exist_ok=True)
    faissdb_index.save_local(result_faiss_path)
    
    txt = "\n".join(faissdbspath)
    # pdf to text 저장
    today=datetime.datetime.today().strftime('%y-%m-%d')
    file = open(os.path.join(result_faiss_path,f"inside_file_{today}.txt"), 'w')
    file.write(txt)
    file.close()

    return [result_faiss_path,faissdbspath]


def textfile2raptorfaiss(filepath:str,chunk_size_set=1000,overlap_set=100,model="OPENAI",api_key=OPENAI_API_KEY,resultpath=None)->str: 
    if resultpath==None or resultpath=='':
        resultpath=os.path.dirname(filepath)
    if os.path.exists(resultpath):
        pass
    else:
        return
    
    embeddings=OpenAIEmbeddings(openai_api_key=api_key)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size_set, chunk_overlap=overlap_set)

    txt=textfile_reader(filepath)
    text = text_splitter.split_text(txt)
    faissdb = FAISS.from_documents(text, embeddings)
    
    basename = os.path.basename(filepath)
    filenames=os.path.splitext(basename)
    filename=filenames[0]

    resultfilepath=os.path.join(resultpath,f"{filename}_index")
    if os.path.exists(resultfilepath):
        pass
    else:
        pass
    faissdb.save_local(resultfilepath)
    return filename