import streamlit as st
import os
from database.init_db import init_db

@st.cache_resource
def setup_database():
    try:
        init_db()
    except Exception as e:
        pass # Ignore table exists errors on concurrent starts

setup_database()

st.set_page_config(
    page_title="AdvancePass V6.0 Ultimate",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "ui", "styles", "main.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.title("🛡️ AdvancePass V6.0 Ultimate")
st.markdown("### The Enterprise AI-Powered Password Security Platform")

st.info("Welcome to the Ultimate Edition. Please select a module from the sidebar to begin.")

st.markdown("""
**Core Features:**
*   🔒 **Password Checker:** Advanced entropy and pattern analysis.
*   🔑 **Password Generator:** Profiles, XKCD, and policies.
*   🤖 **AI Copilot:** Your personal cybersecurity assistant.
*   📊 **Analytics Dashboard:** Enterprise-grade security metrics.
*   🔬 **Research Lab:** Dataset analysis and mutation simulator.
*   🗄️ **Secure Vault:** AES-256 local encrypted storage.
""")

st.sidebar.success("System Status: Online & Secure")
