import streamlit as st

pages = {
    "EPC)PE Engineering GPTs":[],
    "Manual":[
        st.Page("how2use.py", title="HOW to Use GPTs"),
    ],
    "PJT Chatbot" : [
        st.Page("upload_itb.py", title="Upload ITB"),
        st.Page("rfp_toxics.py", title="독소조항 검사"),
        st.Page("client_comment.py", title="Check Client Comment"),
        st.Page("rfP_search.py", title="RFP Search"),
    ],
    "Engineering Chatbot" : [
        st.Page("main_app copy 2.py", title="Engineering Chatbot"),
    ],
    "Q&A" : [
        st.Page("main_app copy.py", title="Q&A"),
    ]
}
pg = st.navigation(pages)
pg.run()