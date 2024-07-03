import streamlit as st
import pandas as pd
import os
from start_sample import llmpage, logopage, pjt_page, team_page

cur_path=os.path.dirname(os.path.realpath(__file__))
asset_path=os.path.join(os.path.dirname(cur_path),"asset")

st.set_page_config(page_title="ITB Toxic Finder", page_icon="📊")
st.title("📊 ITB Toxic Finder")

pjt_page()

if st.session_state['pjts'] == "lumar":
    toxic_xlsx = os.path.join(asset_path,"lumar_toxic.xlsx")
elif st.session_state['pjts'] == "jawa9&10":
    toxic_xlsx = os.path.join(asset_path,"jawa_toxic.xlsx")
elif st.session_state['pjts'] == "samcheok":
    toxic_xlsx = os.path.join(asset_path,"sam_toxic.xlsx")

if toxic_xlsx is not None:
    df = pd.read_excel(toxic_xlsx)
    
    st.write("### Please Find below Toxic Clause")
    st.dataframe(df)
    
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='downloaded_file.csv',
        mime='text/csv',
    )
    if st.button("Submit"):
        st.write("### File Downloaded Successfully!")
    
