import streamlit as st
import pandas as pd
from security.vault import init_vault, load_vault, save_vault, add_entry

st.set_page_config(page_title="Secure Vault | AdvancePass", page_icon="🗄️")
st.title("🗄️ Local Secure Vault")

st.markdown("""
Store your passwords securely in an offline, AES-256 encrypted local vault. 
**No data is sent to the cloud.**
""")

# Vault State Management
if "vault_unlocked" not in st.session_state:
    st.session_state.vault_unlocked = False
    st.session_state.master_pwd = None

if not st.session_state.vault_unlocked:
    st.subheader("Unlock or Initialize Vault")
    master_pwd = st.text_input("Master Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Unlock Vault"):
            try:
                # Attempt to load
                load_vault(master_pwd)
                st.session_state.vault_unlocked = True
                st.session_state.master_pwd = master_pwd
                st.rerun()
            except ValueError as e:
                st.error(str(e))
            except Exception:
                st.error("Failed to unlock. Vault may not exist or password is wrong.")
                
    with col2:
        if st.button("Initialize New Vault"):
            if len(master_pwd) < 8:
                st.warning("Master password must be at least 8 characters.")
            else:
                try:
                    init_vault(master_pwd)
                    st.success("New vault created! You can now unlock it.")
                except Exception as e:
                    st.error(f"Error creating vault: {e}")

else:
    st.success("Vault Unlocked")
    if st.button("Lock Vault"):
        st.session_state.vault_unlocked = False
        st.session_state.master_pwd = None
        st.rerun()
        
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["View Entries", "Add Entry"])
    
    with tab1:
        st.subheader("Your Secure Entries")
        try:
            vault_data = load_vault(st.session_state.master_pwd)
            if not vault_data:
                st.info("Vault is empty.")
            else:
                df = pd.DataFrame(vault_data)
                # Hide passwords in dataframe display, maybe show on click or just display a masked version
                df['password'] = '********'
                st.dataframe(df, use_container_width=True)
                
                # Reveal specific password
                reveal_site = st.selectbox("Reveal password for:", [entry['site'] for entry in vault_data])
                if st.button("Reveal"):
                    for entry in vault_data:
                        if entry['site'] == reveal_site:
                            st.code(entry['password'], language="text")
        except Exception as e:
            st.error("Error reading vault data.")

    with tab2:
        st.subheader("Add New Entry")
        site = st.text_input("Website / Application")
        username = st.text_input("Username / Email")
        pwd = st.text_input("Password", type="password")
        
        if st.button("Save Entry"):
            if site and username and pwd:
                try:
                    add_entry(st.session_state.master_pwd, site, username, pwd)
                    st.success(f"Added {site} to vault.")
                except Exception as e:
                    st.error(f"Failed to add: {e}")
            else:
                st.warning("Please fill all fields.")
