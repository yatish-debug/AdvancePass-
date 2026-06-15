import streamlit as st
import pandas as pd
from security.generator import generate_by_profile, bulk_generate, generate_standard_password, generate_xkcd_passphrase, generate_pronounceable_password

st.set_page_config(page_title="Generator | AdvancePass", page_icon="🔑")
st.title("🔑 Secure Password Generator")

tab1, tab2, tab3 = st.tabs(["Smart Profiles", "Custom Rules", "Bulk Generate"])

with tab1:
    st.subheader("Generate by Profile")
    profile = st.selectbox("Select Security Profile", ["Personal", "Banking", "Corporate", "Developer", "High Security"])
    
    if st.button("Generate from Profile"):
        pwd = generate_by_profile(profile)
        st.code(pwd, language="text")
        st.success("Password generated successfully! Copy it securely.")

with tab2:
    st.subheader("Custom Generator")
    gen_type = st.radio("Type", ["Standard Random", "XKCD Passphrase", "Pronounceable"])
    
    if gen_type == "Standard Random":
        length = st.slider("Length", 8, 128, 16)
        upper = st.checkbox("Uppercase", True)
        lower = st.checkbox("Lowercase", True)
        digits = st.checkbox("Numbers", True)
        special = st.checkbox("Special Characters", True)
        
        if st.button("Generate Custom"):
            st.code(generate_standard_password(length, upper, lower, digits, special), language="text")
            
    elif gen_type == "XKCD Passphrase":
        words = st.slider("Number of Words", 3, 10, 4)
        sep = st.text_input("Separator", "-")
        if st.button("Generate XKCD"):
            st.code(generate_xkcd_passphrase(words, sep), language="text")
            
    elif gen_type == "Pronounceable":
        length = st.slider("Length (approx)", 6, 20, 10)
        if st.button("Generate Pronounceable"):
            st.code(generate_pronounceable_password(length), language="text")

with tab3:
    st.subheader("Bulk Generator")
    count = st.number_input("How many passwords?", min_value=1, max_value=1000, value=10)
    bulk_profile = st.selectbox("Profile for Bulk", ["Personal", "Banking", "Corporate", "Developer", "High Security"], key="bulk_prof")
    
    if st.button("Generate Bulk"):
        passwords = bulk_generate(count, generate_by_profile, bulk_profile)
        df = pd.DataFrame(passwords, columns=["Generated Passwords"])
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='bulk_passwords.csv',
            mime='text/csv',
        )
