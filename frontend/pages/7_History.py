import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.password_service import PasswordService

st.title("🕒 History")

st.markdown("### Password Audit History")

history = PasswordService.get_history()

if history:
    df = pd.DataFrame(history)
    df = df[['id', 'timestamp', 'strength', 'entropy', 'crack_time']]
    
    search_query = st.text_input("Search by Strength (e.g. Strong, Weak)")
    if search_query:
        df = df[df['strength'].str.contains(search_query, case=False, na=False)]
        
    st.dataframe(df)
else:
    st.info("No history available.")
