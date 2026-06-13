import streamlit as st
import sys
import os
import time
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.ai_chat_service import AIChatService
from backend.app.database.db_manager import get_all_chat_threads, save_chat_thread, delete_chat_thread

st.title("🤖 AI Password Advisor")
st.markdown("### Cybersecurity Assistant")

# Initialize session state for chat
if "current_thread_id" not in st.session_state:
    st.session_state.current_thread_id = str(uuid.uuid4())
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Cybersecurity Advisor and IT Assistant. How can I help you today?"}
    ]
    st.session_state.chat_title = "New Conversation"

# Load history
threads = get_all_chat_threads()

with st.sidebar:
    st.markdown("### 🔌 API Status")
    if AIChatService.use_llm:
        st.success("✅ Gemini LLM Connected")
    else:
        st.warning("⚠️ Local Fallback Mode")
        
    st.markdown("---")
    st.markdown("### 💬 Chat History")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_thread_id = str(uuid.uuid4())
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI Cybersecurity Advisor and IT Assistant. How can I help you today?"}
        ]
        st.session_state.chat_title = "New Conversation"
        st.rerun()

    st.markdown("#### Previous Chats")
    for th in threads:
        colA, colB = st.columns([0.8, 0.2])
        with colA:
            if st.button(th['title'], key=f"load_{th['id']}", use_container_width=True):
                st.session_state.current_thread_id = th['id']
                st.session_state.chat_title = th['title']
                st.session_state.messages = th['messages']
                st.rerun()
        with colB:
            if st.button("🗑️", key=f"del_{th['id']}"):
                delete_chat_thread(th['id'])
                if st.session_state.current_thread_id == th['id']:
                    st.session_state.current_thread_id = str(uuid.uuid4())
                    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI Cybersecurity Advisor and IT Assistant. How can I help you today?"}]
                    st.session_state.chat_title = "New Conversation"
                st.rerun()
                
# Display quick action buttons
st.markdown("**Quick Questions:**")
col1, col2, col3 = st.columns(3)

def save_current_state():
    # If this is the first user message, generate a title
    if len(st.session_state.messages) == 3 and st.session_state.chat_title == "New Conversation": # [welcome, user, assistant]
        user_msg = st.session_state.messages[1]['content']
        st.session_state.chat_title = (user_msg[:25] + "...") if len(user_msg) > 25 else user_msg
        
    save_chat_thread(
        st.session_state.current_thread_id, 
        st.session_state.chat_title, 
        st.session_state.messages
    )

def trigger_chat(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = AIChatService.get_response(prompt, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_current_state()
    st.rerun()

with col1:
    if st.button("Generate Passphrase"): trigger_chat("Generate a secure passphrase")
with col2:
    if st.button("Explain Entropy"): trigger_chat("What is password entropy?")
with col3:
    if st.button("NIST Guidelines"): trigger_chat("Explain NIST guidelines")

st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask the AI Advisor a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = AIChatService.get_response(prompt, st.session_state.messages[:-1])
        
        typed_response = ""
        for chunk in full_response.split(" "):
            typed_response += chunk + " "
            time.sleep(0.01)
            message_placeholder.markdown(typed_response + "▌")
        message_placeholder.markdown(typed_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_current_state()
