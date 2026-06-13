import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.password_service import PasswordService

st.title("📈 Analytics")

st.markdown("### Password Security Trends")

history = PasswordService.get_history()

if history:
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Strength Distribution")
        strength_counts = df['strength'].value_counts()
        fig1, ax1 = plt.subplots(figsize=(6,4))
        fig1.patch.set_facecolor('none')
        ax1.set_facecolor('none')
        
        colors = {'Very Weak': '#ff4b4b', 'Weak': '#ffa500', 'Medium': '#ffd700', 'Strong': '#00cc66'}
        plot_colors = [colors.get(x, '#333333') for x in strength_counts.index]
        
        ax1.pie(strength_counts, labels=strength_counts.index, autopct='%1.1f%%', startangle=90, colors=plot_colors, textprops={'color':"w"})
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        st.markdown("#### Entropy Distribution")
        fig2, ax2 = plt.subplots(figsize=(6,4))
        fig2.patch.set_facecolor('none')
        ax2.set_facecolor('none')
        ax2.hist(df['entropy'], bins=10, color='#00d2ff', edgecolor='black')
        ax2.set_xlabel('Entropy (bits)', color='w')
        ax2.set_ylabel('Frequency', color='w')
        ax2.tick_params(colors='w')
        st.pyplot(fig2)

else:
    st.info("No data available for analytics yet. Please analyze some passwords first.")
