import streamlit as st
import pandas as pd
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.password_service import PasswordService
from backend.app.reports.pdf_generator import generate_overall_report

st.title("📑 Reports")

st.markdown("### Export Security Data")

history = PasswordService.get_history()

if history:
    df = pd.DataFrame(history)
    df = df[['id', 'timestamp', 'strength', 'entropy', 'crack_time']]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### CSV Format")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name='advancepass_report.csv',
            mime='text/csv',
        )

    with col2:
        st.markdown("#### JSON Format")
        json_str = df.to_json(orient='records', indent=4)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name='advancepass_report.json',
            mime='application/json',
        )
        
    with col3:
        st.markdown("#### PDF Format")
        stats = PasswordService.get_stats()
        pdf_bytes = generate_overall_report(stats, history)
        st.download_button(
            label="📥 Download Enterprise PDF",
            data=pdf_bytes,
            file_name='advancepass_enterprise_audit.pdf',
            mime='application/pdf',
        )
else:
    st.info("No data available to export.")
