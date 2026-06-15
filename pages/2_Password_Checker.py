import streamlit as st
import hashlib
from security.strength import analyze_password_strength
from ml.predictor import predict_strength
from security.breach import check_breach
from database.session import get_db
from database.models import LogEntry

st.set_page_config(page_title="Password Checker | AdvancePass", page_icon="🛡️")
st.title("🛡️ Advanced Password Checker")

password = st.text_input("Enter a password to analyze:", type="password")

if st.button("Analyze Password") and password:
    with st.spinner("Running deep analysis..."):
        # 1. Rule-based & Entropy Analysis
        strength_data = analyze_password_strength(password)
        
        # 2. ML Prediction
        ml_data = predict_strength(password)
        
        # 3. Breach Check
        breach_data = check_breach(password)
        
        # Log to Database
        db = next(get_db())
        hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
        log_entry = LogEntry(
            password_hash=hashed_pwd,
            strength=str(strength_data["overall_score"]),
            entropy=strength_data["shannon_entropy"],
            crack_time=strength_data["crack_time_display"]
        )
        db.add(log_entry)
        db.commit()

    # Display Results
    st.subheader(f"Overall Score: {strength_data['overall_score']}/100")
    st.progress(strength_data['overall_score'] / 100)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Level", strength_data["risk_level"])
    col2.metric("Shannon Entropy", f"{strength_data['shannon_entropy']} bits")
    col3.metric("Est. Crack Time", strength_data["crack_time_display"])
    
    st.markdown("### 🤖 ML Prediction")
    st.info(f"Machine Learning Model predicts this password is **{ml_data['ml_label']}** (Confidence: {ml_data['confidence']}%)")
    
    st.markdown("### ⚠️ Data Breach Check")
    if breach_data["breached"]:
        st.error(f"WARNING: This password was found {breach_data['count']} times in local breached datasets!")
        st.warning(breach_data["recommendation"])
    else:
        st.success("Good news! This password was not found in the local breached database.")
        
    st.markdown("### 💡 Suggestions for Improvement")
    for suggestion in strength_data["suggestions"]:
        st.markdown(f"- {suggestion}")
