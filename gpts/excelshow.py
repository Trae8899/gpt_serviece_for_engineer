import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excel Viewer & Downloader", page_icon="📊")
st.title("📊 Excel Viewer & Downloader")

uploaded_file = r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\icon\toxic_clause_analysis.xlsx"
pjtname=st.selectbox(
    "PJT NAME",
    ("jawa9&10","lumar","samcheok"),
    )

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    st.write("### Please Find below Toxic Clause")
    st.dataframe(df)
    
    @st.cache
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='downloaded_file.csv',
        mime='text/csv',
    )

    st.write("### File Downloaded Successfully!")
