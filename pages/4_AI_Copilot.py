import streamlit as st
from ai.copilot import AICopilot

st.set_page_config(page_title="AI Copilot | AdvancePass", page_icon="🤖")
st.title("🤖 AI Security Copilot")

st.markdown("""
Your personal AI-powered cybersecurity assistant. Ask general security questions, 
or have it analyze and improve a specific password.
""")

@st.cache_resource
def get_copilot():
    return AICopilot()

copilot = get_copilot()

tab1, tab2 = st.tabs(["Chat Assistant", "Password Improvement Engine"])

with tab1:
    st.subheader("Cybersecurity Q&A")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me about password security, encryption, or best practices..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = copilot.ask_general_question(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("Password Improvement")
    weak_pwd = st.text_input("Enter a weak password:", type="password")
    
    if st.button("Analyze & Improve"):
        if weak_pwd:
            with st.spinner("Analyzing vulnerabilities..."):
                weakness = copilot.explain_weakness(weak_pwd)
                
            with st.spinner("Generating secure alternatives..."):
                improvements = copilot.suggest_improvement(weak_pwd)
                
            st.markdown("### 🔍 Vulnerability Analysis")
            st.info(weakness)
            
            st.markdown("### 🛡️ Suggested Alternatives")
            st.success(improvements)
        else:
            st.warning("Please enter a password.")
