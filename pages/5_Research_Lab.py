import streamlit as st
import pandas as pd
from analytics.dataset import analyze_dataset
from ai.simulation import simulate_dictionary_attack, simulate_bruteforce_attack, simulate_mutation_attack
from analytics.dashboard import detect_reuse_in_list

st.set_page_config(page_title="Research Lab | AdvancePass", page_icon="🔬")
st.title("🔬 Cybersecurity Research Lab")

st.markdown("Analyze datasets, simulate attacks, and research password patterns.")

tab1, tab2, tab3 = st.tabs(["Dataset Analyzer", "Attack Simulation", "Reuse Detection"])

with tab1:
    st.subheader("Leaked Dataset Analyzer")
    st.info("Upload a text file or CSV containing passwords to analyze frequency and structural patterns.")
    uploaded_file = st.file_uploader("Upload Dataset (.txt or .csv)", type=['txt', 'csv'])
    
    if uploaded_file is not None:
        if st.button("Analyze Dataset"):
            with st.spinner("Analyzing..."):
                content = uploaded_file.read()
                results = analyze_dataset(content, uploaded_file.name)
                
            if "error" in results:
                st.error(results["error"])
            else:
                col1, col2 = st.columns(2)
                col1.metric("Total Passwords", f"{results['total_passwords']:,}")
                col2.metric("Avg. Length", results['avg_length'])
                
                st.markdown("### Composition")
                st.write(f"- Contains Uppercase: {results['composition']['has_uppercase']}%")
                st.write(f"- Contains Numbers: {results['composition']['has_numbers']}%")
                st.write(f"- Contains Special Chars: {results['composition']['has_special']}%")
                
                st.markdown("### Most Common Patterns/Words")
                df = pd.DataFrame(results['most_common_words'], columns=["Pattern", "Frequency"])
                st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Attack Simulator")
    st.write("Understand how attackers crack passwords by simulating attacks.")
    target_pwd = st.text_input("Target Password:")
    
    if st.button("Run Simulations"):
        if target_pwd:
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("#### Dictionary Attack")
                dict_res = simulate_dictionary_attack(target_pwd)
                if dict_res["success"]:
                    st.error(f"Failed! Broken in {dict_res['estimated_time_seconds']}s")
                else:
                    st.success("Resisted Dictionary Attack.")
                st.caption(dict_res["description"])
                
                st.markdown("#### Brute-Force Attack")
                brute_res = simulate_bruteforce_attack(target_pwd)
                if brute_res["success"]:
                    st.warning(f"Vulnerable! Broken in ~{int(brute_res['estimated_time_seconds'])} seconds")
                else:
                    st.success("Resisted Brute-Force. Unfeasible to crack.")
                st.caption(brute_res["description"])
                
            with col_b:
                st.markdown("#### Mutation Attack (Attacker Mindset)")
                mut_res = simulate_mutation_attack(target_pwd)
                st.caption(mut_res["description"])
                for m in mut_res["mutations_generated"]:
                    st.code(m, language="text")
        else:
            st.warning("Please enter a target password.")

with tab3:
    st.subheader("Password Reuse Detection")
    st.write("Upload a list of passwords to check for reuse (e.g., from an organization's internal audit).")
    reuse_file = st.file_uploader("Upload List (.txt)", type=['txt'])
    
    if reuse_file is not None:
        if st.button("Analyze Reuse"):
            content = reuse_file.read().decode('utf-8', errors='ignore')
            passwords = [line.strip() for line in content.splitlines() if line.strip()]
            
            res = detect_reuse_in_list(passwords)
            st.metric("Reuse Rate", f"{res['reuse_percentage']}%")
            st.write(f"Found {res['reused_count']} reused instances among {res['total_passwords']} total passwords.")
            
            if res['reused_details']:
                st.write("Most Reused Passwords (Top 10):")
                sorted_reuse = sorted(res['reused_details'].items(), key=lambda x: x[1], reverse=True)[:10]
                df_reuse = pd.DataFrame(sorted_reuse, columns=["Password", "Occurrences"])
                st.dataframe(df_reuse, use_container_width=True)
