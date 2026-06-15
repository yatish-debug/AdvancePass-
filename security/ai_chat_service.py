import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from backend.app.services.password_service import PasswordService

load_dotenv()

class AIChatService:
    # Set up Gemini model
    api_key = os.getenv("GEMINI_API_KEY")
    use_llm = False
    model = None

    if api_key and api_key != "your_gemini_api_key_here":
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash for fast text responses
        model = genai.GenerativeModel('gemini-2.5-flash',
            system_instruction=(
                "You are the AdvancePass v5.0 AI Advisor, a Senior Cybersecurity Architect and IT Assistant. "
                "Your primary role is to teach users about password security, entropy, NIST/OWASP guidelines, "
                "and explain password vulnerabilities. "
                "You are also capable of acting as a General IT Assistant to answer broad technology questions. "
                "Keep your answers professional, structured with markdown (bullet points/bold text), and highly accurate."
            )
        )
        use_llm = True

    @staticmethod
    def get_response(prompt: str, history: list = None) -> str:
        prompt_lower = prompt.lower().strip()
        
        # Always hook passphrase generation natively for security (don't rely on LLM for random generation)
        if re.search(r'\b(generate|create|make).+(passphrase|password)\b', prompt_lower) or 'passphrase' in prompt_lower:
            passphrase = PasswordService.generate_memorable(words=4, separator='-')
            return (
                "Here is a highly secure, contextually generated passphrase for you:\n\n"
                f"**`{passphrase}`**\n\n"
                "Passphrases use random dictionary words. They are incredibly strong against brute-force attacks "
                "because their length creates massive entropy, while still being easy for a human to remember."
            )

        if AIChatService.use_llm:
            try:
                # Convert our Streamlit history format to Gemini format
                gemini_history = []
                if history:
                    for msg in history:
                        # Skip the initial welcome message from the assistant or system messages
                        if msg["role"] == "user":
                            gemini_history.append({"role": "user", "parts": [msg["content"]]})
                        elif msg["role"] == "assistant":
                            gemini_history.append({"role": "model", "parts": [msg["content"]]})

                chat = AIChatService.model.start_chat(history=gemini_history)
                response = chat.send_message(prompt)
                return response.text
            except Exception as e:
                return f"⚠ LLM Error: {e}\n\nFalling back to local engine..."

        # Fallback Local Rule-Based Engine
        return AIChatService._get_local_response(prompt_lower)

    @staticmethod
    def _get_local_response(prompt: str) -> str:
        if 'entropy' in prompt:
            return (
                "**Password Entropy** is a mathematical measurement of how unpredictable a password is. "
                "It is measured in 'bits'. The formula is: `E = L × log2(R)` where `L` is the password length "
                "and `R` is the size of the character pool (lowercase, uppercase, numbers, symbols).\n\n"
                "- **< 40 bits**: Very Weak (easily cracked)\n"
                "- **40 - 60 bits**: Moderate (acceptable for low-risk)\n"
                "- **> 60 bits**: Strong (highly resistant to cracking)\n"
                "To increase your entropy, the most effective method is simply to **make your password longer**!"
            )
            
        if 'nist' in prompt:
            return (
                "The **NIST SP 800-63B** guidelines represent the modern standard for digital identity and password security. "
                "Key recommendations include:\n\n"
                "1. **Length over Complexity**: Minimum 8 characters, but strongly encourages longer passphrases.\n"
                "2. **No Arbitrary Rules**: Stop requiring a mix of uppercase, lowercase, numbers, and symbols if it forces users to create predictable patterns.\n"
                "3. **No Expiration**: Stop forcing users to change passwords every 90 days.\n"
                "4. **Breach Checking**: Passwords *must* be checked against known compromised databases."
            )
            
        if 'owasp' in prompt:
            return (
                "The **OWASP Application Security Verification Standard (ASVS)** recommends:\n\n"
                "1. Enforcing a minimum password length of **12 characters**.\n"
                "2. Allowing a maximum length of at least 64 characters.\n"
                "3. Checking new passwords against a list of the top 100,000 most common compromised passwords."
            )
            
        if 'weak' in prompt or 'mistake' in prompt:
            return (
                "The most common password weaknesses include:\n\n"
                "- **Dictionary Words**: Using names or dictionary words.\n"
                "- **Predictable Mutations**: Using 'leet speak' (e.g., `P@ssw0rd`).\n"
                "- **Password Reuse**: The most critical weakness!"
            )
            
        if 'policy' in prompt or 'enterprise' in prompt:
            return (
                "For a modern **Enterprise Password Policy**, I recommend:\n\n"
                "1. **Enforce MFA**: Multi-Factor Authentication is non-negotiable.\n"
                "2. **Minimum 12 Characters**: Mandate 12+ characters.\n"
                "3. **Real-time Breach Checking**: Deny the creation of breached passwords."
            )
            
        return (
            "*(Local Fallback Mode)* I am AdvancePass's AI Cybersecurity Advisor! "
            "I can help you understand security concepts, explain guidelines like NIST or OWASP, "
            "recommend enterprise policies, or generate a secure passphrase. "
            "To unlock my full Generative AI capabilities for general IT questions, please add your Gemini API Key to the `.env` file."
        )
