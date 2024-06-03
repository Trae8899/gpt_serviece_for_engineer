import dotenv 

from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.llms.llamacpp import LlamaCpp
from langchain_community.embeddings.llamacpp import LlamaCppEmbeddings

from langchain.vectorstores.faiss import FAISS
from gpt_servieces.doc_reader import textfile_reader
import datetime

project_path=os.path.dirname(os.path.dirname(__file__))
drive_path = "llms"  # 사용자의 실제 하드 드라이브 경로로 수정해주세요.
model_basename = "ggml-model-Q4_K_M.gguf" # file name
destination_path = os.path.join(project_path,drive_path, model_basename)
llama_path=destination_path

store = LocalFileStore("./cache/")
# embeddings 인스턴스를 생성합니다.

def textfile2faiss(filepath:str,chunk_size_set=512,overlap_set=50,resultpath=None,model_path=llama_path): 
    embd = LlamaCppEmbeddings(model_path=model_path)

    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embd, store, namespace="llama512"
    )
    if os.path.exists(filepath):
        print("file is exist")
        print(filepath)
    else:
        print("file is not in here")
        return
    print(resultpath)
    if resultpath==None or resultpath=='':
        resultpath=os.path.dirname(filepath)
    print(os.path.exists(resultpath))
    if os.path.exists(resultpath):
        print(resultpath)
        pass
    else:
        print(resultpath)
        return
    

    print("------------babsab")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size_set, chunk_overlap=overlap_set)

    txt=textfile_reader(filepath)
    print("------------")
    print(txt)
    print("------------")
    text = text_splitter.split_text(txt)
    
    faissdb = FAISS.from_texts(text, cached_embeddings)
    
    basename = os.path.basename(filepath)
    filenames=os.path.splitext(basename)
    filename=filenames[0]

    resultfilepath=os.path.join(resultpath,f"{filename}_index")
    if os.path.exists(resultfilepath):
        pass
    else:
        pass
    faissdb.save_local(resultfilepath)
    return resultfilepath

def merge_faiss(faissfolderpaths,resultpath=None,name=None,model_path=llama_path):
    embd = LlamaCppEmbeddings(model_path=model_path)

    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embd, store, namespace="llama512"
    )
    if len(faissfolderpaths) <1:
        return
    if name==None:
        name="faiss_index"
    if resultpath==None:
        resultpath=os.path.dirname(faissfolderpaths[0])

    faissdbs=[]
    faissdbspath=[]
    for faisspath in faissfolderpaths:
        try:
            faissdb = FAISS.load_local(faisspath,embeddings=cached_embeddings,allow_dangerous_deserialization="True")
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


def textfile2raptorfaiss(filepath:str,chunk_size_set=512,overlap_set=100,resultpath=None,model_path=llama_path)->str: 
    if resultpath==None or resultpath=='':
        resultpath=os.path.dirname(filepath)
    if os.path.exists(resultpath):
        pass
    else:
        return
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size_set, chunk_overlap=overlap_set)

    txt=textfile_reader(filepath)
    text = text_splitter.split_text(txt)

    embd = LlamaCppEmbeddings(model_path=model_path)

    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embd, store, namespace="llama512"
    )
    
    faissdb = FAISS.from_documents(text, cached_embeddings)
    
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

def faiss2txt(resultpath=None,model_path=llama_path)->str: 
    if resultpath==None or resultpath=='':
        return
    if os.path.exists(resultpath):
        pass
    else:
        return
    embd = LlamaCppEmbeddings(model_path=model_path)

    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embd, store, namespace="llama512"
    )
    vectordb = FAISS.load_local(resultpath,cached_embeddings,allow_dangerous_deserialization=True)
    
    return vectordb