import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from database.session import get_db
from analytics.dashboard import get_overall_metrics, get_entropy_distribution

from reports.generator import generate_dashboard_pdf
import os

st.set_page_config(page_title="Dashboard | AdvancePass", page_icon="📊", layout="wide")

col_header, col_dl = st.columns([8, 2])
with col_header:
    st.title("📊 Enterprise Security Dashboard")

db = next(get_db())
metrics = get_overall_metrics(db)

import tempfile

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Passwords Analyzed", metrics["total"])
col2.metric("Average Security Score", f"{metrics['avg_score']}/100")
col3.metric("Weak Passwords Detected", metrics["weak_count"], delta_color="inverse")
col4.metric("Strong Passwords", metrics["strong_count"], delta_color="normal")

st.markdown("---")

# Pre-generate Charts
labels = ['Weak', 'Moderate', 'Strong']
moderate_count = metrics["total"] - metrics["weak_count"] - metrics["strong_count"]
values = [metrics["weak_count"], max(0, moderate_count), metrics["strong_count"]]

fig1 = px.pie(values=values, names=labels, color=labels,
             color_discrete_map={'Weak': '#ef4444', 'Moderate': '#f59e0b', 'Strong': '#10b981'},
             hole=0.4)
fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")

entropies = get_entropy_distribution(db)
fig2 = None
if entropies:
    fig2 = px.histogram(x=entropies, nbins=20, labels={'x': 'Shannon Entropy', 'y': 'Count'})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    fig2.update_traces(marker_color='#3b82f6')

with col_dl:
    st.write("") # Padding
    st.write("")
    # Save charts to temp files for PDF
    chart1_path = os.path.join(tempfile.gettempdir(), "chart1.png")
    chart2_path = os.path.join(tempfile.gettempdir(), "chart2.png")
    
    # We change background to white specifically for the PDF export so it's visible on paper
    fig1_pdf = px.pie(values=values, names=labels, color=labels, color_discrete_map={'Weak': '#ef4444', 'Moderate': '#f59e0b', 'Strong': '#10b981'}, hole=0.4)
    fig1_pdf.write_image(chart1_path, width=500, height=400)
    
    if fig2:
        fig2_pdf = px.histogram(x=entropies, nbins=20, labels={'x': 'Shannon Entropy', 'y': 'Count'})
        fig2_pdf.update_traces(marker_color='#3b82f6')
        fig2_pdf.write_image(chart2_path, width=500, height=400)
    else:
        chart2_path = None
        
    pdf_path = generate_dashboard_pdf(metrics, chart1_path, chart2_path)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download PDF Report",
            data=f.read(),
            file_name="Dashboard_Metrics.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Render Charts in UI
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Strength Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("Entropy Distribution")
    if fig2:
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No data available yet. Analyze some passwords to see the entropy distribution.")
