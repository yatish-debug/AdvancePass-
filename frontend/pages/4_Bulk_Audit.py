import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.password_service import PasswordService

st.title("📁 Bulk Password Audit")

st.markdown("""
Upload a CSV file containing a column named `password` (or where the first column is the passwords).
The system will audit all passwords and generate a consolidated report using the hybrid evaluation engine.
""")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        # Try to find a password column
        pwd_col = None
        for col in df.columns:
            if 'password' in col.lower():
                pwd_col = col
                break
        
        if not pwd_col:
            pwd_col = df.columns[0] # Default to first column
            st.warning(f"No 'password' column found. Using '{pwd_col}' as the password column.")
            
        passwords = df[pwd_col].dropna().astype(str).tolist()
        
        if st.button(f"Audit {len(passwords)} Passwords"):
            results = []
            progress_bar = st.progress(0)
            
            for i, pwd in enumerate(passwords):
                try:
                    res = PasswordService.check_password(pwd)
                    results.append({
                        "Password_Length": len(pwd),
                        "Strength": res.security_level,
                        "Score": res.composite_score,
                        "Entropy": res.entropy,
                        "Crack_Time": res.crack_time,
                        "HIBP_Count": res.hibp_count,
                        "NIST_Compliant": bool(res.nist_compliance),
                        "OWASP_Compliant": bool(res.owasp_compliance),
                        "Is_Reused": res.password_reuse_detected
                    })
                except Exception as e:
                    results.append({
                        "Password_Length": len(pwd),
                        "Strength": "Error",
                        "Score": 0,
                        "Entropy": 0.0,
                        "Crack_Time": "N/A",
                        "HIBP_Count": 0,
                        "NIST_Compliant": False,
                        "OWASP_Compliant": False,
                        "Is_Reused": False
                    })
                progress_bar.progress((i + 1) / len(passwords))
                
            results_df = pd.DataFrame(results)
            st.success("Audit Complete!")
            
            st.markdown("### Audit Summary")
            col1, col2, col3 = st.columns(3)
            # Filter out error rows for mean calculation
            valid_df = results_df[results_df['Strength'] != 'Error']
            
            if not valid_df.empty:
                col1.metric("Average Score", f"{valid_df['Score'].mean():.2f}")
                col2.metric("Breached Passwords", int((valid_df['HIBP_Count'] > 0).sum()))
                col3.metric("NIST Non-Compliant", int((~valid_df['NIST_Compliant']).sum()))
            
            st.dataframe(results_df)
            
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Audit Report (CSV)",
                data=csv,
                file_name='bulk_audit_report.csv',
                mime='text/csv',
            )

    except Exception as e:
        st.error(f"⚠ An unexpected error occurred while processing the file: {e}")
