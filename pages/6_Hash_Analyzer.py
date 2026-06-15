import streamlit as st
from security.hash_analyzer import analyze_hash

st.set_page_config(page_title="Hash Analyzer | AdvancePass", page_icon="#️⃣")
st.title("#️⃣ Educational Hash Analyzer")

st.markdown("""
Paste a password hash here to identify the algorithm, understand its security properties, 
and learn about modern password hashing alternatives.
""")

hash_input = st.text_input("Enter Hash String:")

if st.button("Analyze Hash"):
    if hash_input:
        with st.spinner("Identifying hash..."):
            result = analyze_hash(hash_input)
            
        st.subheader(f"Algorithm Detected: {result['algorithm']}")
        
        rating_color = "green" if result['security_rating'] in ["Strong", "Excellent"] else "red"
        st.markdown(f"**Security Rating:** <span style='color:{rating_color}'>{result['security_rating']}</span>", unsafe_allow_html=True)
        
        st.markdown("### 📚 Explanation")
        st.info(result['explanation'])
        
        st.markdown("### 💡 Recommended Alternative")
        st.success(result['recommended_alternative'])
    else:
        st.warning("Please enter a hash string to analyze.")
