import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.password_service import PasswordService

st.title("🎲 Password Generator")

tab1, tab2, tab3 = st.tabs(["Random Secure", "Memorable", "Passphrase"])

with tab1:
    st.markdown("### Random Secure Password")
    length = st.slider("Password Length", min_value=12, max_value=64, value=16)
    col1, col2 = st.columns(2)
    with col1:
        inc_upper = st.checkbox("Include Uppercase", value=True)
        inc_lower = st.checkbox("Include Lowercase", value=True)
    with col2:
        inc_digits = st.checkbox("Include Digits", value=True)
        inc_symbols = st.checkbox("Include Symbols", value=True)
        
    exc_ambig = st.checkbox("Exclude Ambiguous (0,O,I,l,1)", value=False)
    
    if st.button("Generate Random Password"):
        pwd = PasswordService.generate_random_password(length, inc_upper, inc_lower, inc_digits, inc_symbols, exc_ambig)
        st.code(pwd, language="text")

with tab2:
    st.markdown("### Memorable Password")
    words = st.slider("Number of Words", min_value=3, max_value=8, value=4)
    sep = st.text_input("Separator", value="-", max_chars=1)
    
    if st.button("Generate Memorable Password"):
        pwd = PasswordService.generate_memorable(words, sep)
        st.code(pwd, language="text")

with tab3:
    st.markdown("### XKCD-Style Passphrase")
    words_pp = st.slider("Number of Words (Passphrase)", min_value=4, max_value=12, value=4)
    sep_pp = st.text_input("Passphrase Separator", value=" ", max_chars=1)
    
    if st.button("Generate Passphrase"):
        pwd = PasswordService.generate_memorable(words_pp, sep_pp)
        st.code(pwd, language="text")
