import streamlit as st
import sys
import os
import pandas as pd

# Add the root directory to sys.path so we can import backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.services.password_service import PasswordService

st.title("📊 Dashboard")

st.markdown("### Security Overview")

stats = PasswordService.get_stats()
history = PasswordService.get_history()

total_analyzed = len(history)

# Count strengths
strength_counts = {"Very Weak": 0, "Weak": 0, "Medium": 0, "Strong": 0}
for row in stats:
    if row[0] in strength_counts:
        strength_counts[row[0]] = row[1]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stCard"><div class="stat-label">Total Analyzed</div><div class="stat-value">{total_analyzed}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stCard"><div class="stat-label">Strong</div><div class="stat-value" style="color:#00cc66">{strength_counts["Strong"]}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stCard"><div class="stat-label">Medium</div><div class="stat-value" style="color:#ffd700">{strength_counts["Medium"]}</div></div>', unsafe_allow_html=True)
with col4:
    weak_count = strength_counts["Very Weak"] + strength_counts["Weak"]
    st.markdown(f'<div class="stCard"><div class="stat-label">Weak / Very Weak</div><div class="stat-value" style="color:#ff4b4b">{weak_count}</div></div>', unsafe_allow_html=True)

st.markdown("### Recent Activity")
if history:
    # Display last 5
    df = pd.DataFrame(history[:5])
    st.dataframe(df[['timestamp', 'strength', 'entropy', 'crack_time']])
else:
    st.info("No passwords analyzed yet.")
