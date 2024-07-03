import streamlit as st
from streamlit_feedback import streamlit_feedback
from start_sample import llmpage, logopage, pjt_page, team_page

st.set_page_config(page_title="Client Comment", page_icon="🦜")

st.title("🦜 Client Comment checker")
st.caption("🚀 chatbot powered by AI")
logopage()
pjt_page()
team_page()
reset_history = st.sidebar.button("Reset chat history")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "ai", "content": "How can I help you?"}]
    st.session_state.feedback_scores = []
    st.session_state.last_response = None

feedback_kwargs = {
    "feedback_type": "faces",
    "optional_text_label": "[Optional] Please provide an explanation",
}

def get_feedback(index):
    feedback_key = f"feedback_{index}"
    if feedback_key not in st.session_state:
        st.session_state[feedback_key] = None
    feedback = streamlit_feedback(**feedback_kwargs, key=feedback_key)
    if feedback:
        scores = {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0}
        score = scores[feedback["score"]]
        st.session_state.feedback_scores.append({"index": index, "score": score, "comment": feedback.get("text", "")})
        if feedback.get("text"):
            st.write(f"Comment: {feedback['text']}")

for n, msg in enumerate(st.session_state.messages):
    avatar = "🦜" if msg["role"] == "ai" else None
    st.chat_message(msg["role"]).write(msg["content"])
    if msg["role"] == "ai" and n > 0:  # Skip the initial message
        get_feedback(n)

MAX_CHAR_LIMIT = 500  # Adjust this value as needed

if prompt := st.chat_input():
    if len(prompt) > MAX_CHAR_LIMIT:
        st.warning(f"⚠️ Your input is too long! Please limit your input to {MAX_CHAR_LIMIT} characters.")
        prompt = None  # Reset the prompt so it doesn't get processed further
    else:
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = "i don't know"
        st.session_state.messages.append({"role": "ai", "content": response})
        st.chat_message("ai").write(response)
        get_feedback(len(st.session_state.messages) - 1)  # Request feedback immediately after response

def adjust_response_based_on_feedback(response, feedback_scores):
    if not feedback_scores:
        return response

    latest_feedback = feedback_scores[-1]
    score = latest_feedback["score"]
    
    if score < 0.5:
        return "I'm sorry if my previous responses were not helpful. How can I assist you better?"
    elif score < 0.75:
        return "I'll try to improve my responses. What else would you like to know?"
    else:
        return response

if st.session_state.messages and st.session_state.feedback_scores:
    last_response = st.session_state.messages[-1]["content"]
    adjusted_response = adjust_response_based_on_feedback(last_response, st.session_state.feedback_scores)
    if adjusted_response != last_response:
        st.write(f"Adjusted response: {adjusted_response}")
