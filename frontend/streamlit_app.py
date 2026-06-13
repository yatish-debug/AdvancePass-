import streamlit as st
import os

# Set page config globally
st.set_page_config(
    page_title="AdvancePass v5.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles", "main.css")
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

st.title("🛡️ AdvancePass Enterprise")
st.markdown("### Welcome to the AdvancePass Password Security & Audit Platform")

st.info("👈 Please select a module from the sidebar to get started.")

st.markdown("""
---
**Features:**
- **Dashboard:** Overview of password security metrics.
- **Password Checker:** Real-time analysis with AI advice.
- **Password Generator:** Generate secure & memorable passwords.
- **Bulk Audit:** Evaluate multiple passwords at once.
- **Analytics:** Visual statistics of your password history.
- **History & Reports:** View and export your security audits.
""")
