import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.password_service import PasswordService

st.title("⚙️ Settings")

st.markdown("### Application Preferences")

st.info("Settings will be fully functional in Phase 4 (User Management) & Phase 7 (Compliance).")

st.markdown("#### Theme")
theme_choice = st.selectbox("Select Theme", ["Dark (Glassmorphism)", "Light", "System Default"])

st.markdown("#### Password Policies")
min_length = st.number_input("Minimum Password Length", min_value=8, max_value=128, value=12)
req_upper = st.checkbox("Require Uppercase", value=True)
req_lower = st.checkbox("Require Lowercase", value=True)
req_digits = st.checkbox("Require Digits", value=True)
req_symbols = st.checkbox("Require Symbols", value=True)

st.markdown("#### Database Management")
if st.button("Clear History"):
    try:
        PasswordService.clear_database()
        st.success("Database cleared successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to clear database: {e}")
