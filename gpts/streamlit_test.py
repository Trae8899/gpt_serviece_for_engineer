import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
add_page_title()

show_pages(
    [   
        
        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\Course_Overview.py", "DE Zoomcamp", "💻",in_section=False),

        # GPT 사용법
        Section("DE Zoomcamp 2023", "👨‍🔧"),
        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\page2\Week_2_Workflow_Orchestration.py", "Course Overview", "📚", in_section=True),
        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\page2\Week_1_Introduction_&_Prerequisites.py", "1️⃣", in_section=True),

        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\page2\Week_6_Stream_Processing.py", "aaa21", "❔", in_section=False),
        Page(r"C:\Users\qkrwo\Documents\Digital\JPark\gpt_serviece_for_engineer\tests\page2\Week_7_Project.py", "FAQ", "❔", in_section=False),

    ]
)

hide_pages(["Thank you"])

st.markdown("### 👨‍🔧 Data Engineering Zoomcamp by [DataTalksClub](https://datatalks.club/)")

st.image("https://pbs.twimg.com/media/FmmYA2YWYAApPRB.png")

st.info("Original Course Repository on [Github](https://github.com/DataTalksClub/data-engineering-zoomcamp)")

st.markdown("---")

with st.expander("Sign up here for 2024 Cohort"):
    st.markdown("""
    
    <a href="https://airtable.com/appzbS8Pkg9PL254a/shr6oVXeQvSI5HuWD"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>

    #

    - Register in [DataTalks.Club's Slack](https://datatalks.club/slack.html)
    - Join the [`#course-data-engineering`](https://app.slack.com/client/T01ATQK62F8/C01FABYF2RG) channel
    - Join the [course Telegram channel with announcements](https://t.me/dezoomcamp)
    - The videos are published on [DataTalks.Club's YouTube channel](https://www.youtube.com/c/DataTalksClub) in [the course playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
    - [Frequently asked technical questions](https://docs.google.com/document/d/19bnYs80DwuUimHM65UV3sylsCn2j1vziPOwzBwQrebw/edit?usp=sharing)
        
    #""", unsafe_allow_html=True)

st.markdown("""
### 👨‍🎓 Taking the course

##### 👨‍👦‍👦 2024 Cohort

* **Start**: 15 January 2024 (Monday) at 17:00 CET
* **Registration link**: https://airtable.com/shr6oVXeQvSI5HuWD
* [Cohort folder](cohorts/2024/) with homeworks and deadlines 


##### 👨‍🔧 Self-paced mode

All the materials of the course are freely available, so that you
can take the course at your own pace

* Follow the suggested syllabus (see below) week by week
* You don't need to fill in the registration form. Just start watching the videos and join Slack
* Check [FAQ](https://docs.google.com/document/d/19bnYs80DwuUimHM65UV3sylsCn2j1vziPOwzBwQrebw/edit?usp=sharing) if you have problems
* If you can't find a solution to your problem in FAQ, ask for help in Slack

### 🔎 Overview""", unsafe_allow_html=True)


st.image("https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/images/architecture/photo1700757552.jpeg")


st.markdown("""
### 📓 Prerequisites

Prior experience with data engineering is not required.

### 👨‍🏫 Instructors

- [Luis Oliveira](https://www.linkedin.com/in/lgsoliveira/)
- [Michael Shoemaker](https://www.linkedin.com/in/michaelshoemaker1/)

Past instructors:

- [Irem Erturk](https://www.linkedin.com/in/iremerturk/)

### ❔ Asking for help in Slack

To make discussions in Slack more organized:

* Follow [these recommendations](asking-questions.md) when asking for help
* Read the [DataTalks.Club community guidelines](https://datatalks.club/slack/guidelines.html)

---
            
### ⭐ Star the project on Github  <iframe src="https://ghbtns.com/github-btn.html?user=hamagistral&repo=de-zoomcamp-ui&type=star&count=true"  width="150" height="20" title="GitHub"></iframe>   
            
##### 🖼️ Course UI was made by [Hamagistral](https://github.com/Hamagistral) 
""", unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 