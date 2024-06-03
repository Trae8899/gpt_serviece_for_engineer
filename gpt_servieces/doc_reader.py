import re
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.word_document import UnstructuredWordDocumentLoader
import os


def textfile_reader(filepath:str)->str:
    print("afkjadslkfja;lsdkfja;sldkj")
    basename = os.path.basename(filepath)
    filenames=os.path.splitext(basename)
    ext=filenames[1]
    filename=filenames[0]
    print(ext)
    if ext.upper()==".PDF":
        loader = PyMuPDFLoader(filepath)
    elif ext.upper()==".DOCX"|".DOC":
        loader = UnstructuredWordDocumentLoader(filepath)
    else:
        return
    document = loader.load()
    
    ext_text = "" 
    temp = ""

    for i in document:
        print(i)
        temp = i.page_content
        temp = temp.replace("\n", " ")
        ext_text = ext_text + temp
        temp = ""

    txt = ""
    final_sent = re.compile("[a-z]*\.")

    for i in range(len(ext_text)):
        txt = txt + ext_text[i]
        m = final_sent.findall(ext_text[i])
        if m:
            txt = txt + "\n"
    return txt

