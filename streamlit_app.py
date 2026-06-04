import os
import streamlit as st
from dotenv import load_dotenv
from memory import ConversationMemory
from guardrails import input_guardrail, system_prompt
from oss_assistant import OSSAssistant
from frontier_assistant import FrontierAssistant

load_dotenv()
st.set_page_config(page_title="Dual AI Personal Assistant", page_icon="🤖")
st.title("Dual AI Personal Assistant")
st.caption("Compare an open-source Hugging Face assistant with a hosted frontier model assistant.")

mode = st.sidebar.selectbox("Assistant backend", ["Open Source - Hugging Face", "Frontier - OpenAI API"])
max_turns = st.sidebar.slider("Short-term memory turns", 2, 12, 6)

if "memory" not in st.session_state or st.sidebar.button("Reset conversation"):
    st.session_state.memory = ConversationMemory(max_turns=max_turns)
    st.session_state.chat_log = []

@st.cache_resource(show_spinner=True)
def load_oss():
    return OSSAssistant()

@st.cache_resource(show_spinner=True)
def load_frontier():
    return FrontierAssistant()

for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_msg = st.chat_input("Ask your assistant...")
if user_msg:
    ok, blocked = input_guardrail(user_msg)
    st.session_state.memory.add("user", user_msg)
    st.session_state.chat_log.append({"role":"user","content":user_msg})
    with st.chat_message("user"):
        st.write(user_msg)
    with st.chat_message("assistant"):
        if not ok:
            answer = blocked
        else:
            messages = [{"role":"system", "content": system_prompt()}] + st.session_state.memory.get()
            assistant = load_oss() if mode.startswith("Open") else load_frontier()
            answer = assistant.chat(messages)
        st.write(answer)
    st.session_state.memory.add("assistant", answer)
    st.session_state.chat_log.append({"role":"assistant","content":answer})
