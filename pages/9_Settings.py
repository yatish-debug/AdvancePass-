import streamlit as st
import os

st.set_page_config(page_title="Settings | AdvancePass", page_icon="⚙️")
st.title("⚙️ System Settings")

st.markdown("""
Configure your local environment and API keys. These settings are stored locally in your `.env` file.
""")

env_path = os.path.join(os.path.dirname(__file__), "..", "config", ".env")

def load_env():
    envs = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    envs[k] = v
    return envs

def save_env(envs):
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    with open(env_path, "w") as f:
        for k, v in envs.items():
            f.write(f"{k}={v}\n")

current_envs = load_env()

st.subheader("🤖 AI Integration Settings")

gemini_key = st.text_input("Google Gemini API Key (Optional for Free API)", value=current_envs.get("GEMINI_API_KEY", ""), type="password")
ollama_url = st.text_input("Ollama Local URL", value=current_envs.get("OLLAMA_URL", "http://localhost:11434/api/generate"))
ollama_model = st.text_input("Ollama Model Name", value=current_envs.get("OLLAMA_MODEL", "llama3"))

if st.button("Save Settings"):
    current_envs["GEMINI_API_KEY"] = gemini_key
    current_envs["OLLAMA_URL"] = ollama_url
    current_envs["OLLAMA_MODEL"] = ollama_model
    save_env(current_envs)
    st.success("Settings saved successfully! You may need to restart the application for some changes to take effect.")

st.markdown("---")
st.subheader("🗄️ Database Management")
st.markdown("Clear all saved password analysis history and AI chat threads. **This action cannot be undone.**")

if st.button("Clear Database History", type="primary"):
    from database.session import get_db
    from database.models import LogEntry, ChatThread
    db = next(get_db())
    try:
        db.query(LogEntry).delete()
        db.query(ChatThread).delete()
        db.commit()
        st.success("Database history cleared successfully!")
    except Exception as e:
        db.rollback()
        st.error(f"Failed to clear database: {e}")

