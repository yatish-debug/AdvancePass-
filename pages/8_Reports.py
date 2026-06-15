import streamlit as st
import os
from database.session import get_db
from analytics.dashboard import get_recent_history
from reports.generator import generate_csv_report, generate_json_report, generate_pdf_report, generate_docx_report

st.set_page_config(page_title="Reports | AdvancePass", page_icon="📄")
st.title("📄 Professional Reports & Export")

st.markdown("""
Generate and download professional security audit reports in various formats.
These reports include your recent password analysis history and metrics.
""")

db = next(get_db())
recent_logs = get_recent_history(db, limit=50)

if not recent_logs:
    st.info("No analysis history found. Analyze some passwords first.")
else:
    # Prepare data for export
    export_data = []
    for log in recent_logs:
        export_data.append({
            "Timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Strength Score": log.strength,
            "Shannon Entropy": log.entropy,
            "Est. Crack Time": log.crack_time
        })
        
    st.subheader("Export Formats")
    format_choice = st.radio("Select Format", ["CSV", "JSON", "PDF", "DOCX"])
    
    if st.button("Generate Report"):
        with st.spinner(f"Generating {format_choice} report..."):
            filepath = ""
            if format_choice == "CSV":
                filepath = generate_csv_report(export_data)
            elif format_choice == "JSON":
                filepath = generate_json_report(export_data)
            elif format_choice == "PDF":
                filepath = generate_pdf_report(export_data)
            elif format_choice == "DOCX":
                filepath = generate_docx_report(export_data)
                
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    file_bytes = f.read()
                    
                st.success("Report generated successfully!")
                st.download_button(
                    label=f"Download {format_choice}",
                    data=file_bytes,
                    file_name=os.path.basename(filepath),
                    mime="application/octet-stream"
                )
            else:
                st.error("Failed to generate report.")
