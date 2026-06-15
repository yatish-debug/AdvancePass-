import os
import requests
import google.generativeai as genai
from security.strength import analyze_password_strength

def _load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), "..", "config", ".env")
    envs = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    envs[k] = v
    return envs

class AICopilot:
    def __init__(self):
        envs = _load_env_file()
        self.gemini_api_key = envs.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.ollama_url = envs.get("OLLAMA_URL") or os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.ollama_model = envs.get("OLLAMA_MODEL") or os.getenv("OLLAMA_MODEL", "llama3")
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            
    def _generate_response(self, prompt: str) -> str:
        """Tries Ollama first, then Gemini, then fallback."""
        # Try Ollama (Local)
        try:
            response = requests.post(self.ollama_url, json={
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }, timeout=5)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except Exception:
            pass # Ollama not available
            
        # Try Gemini (Free API if configured)
        if self.gemini_api_key:
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
            except Exception:
                pass
                
        # Rule-based fallback
        return self._rule_based_fallback(prompt)
        
    def _rule_based_fallback(self, prompt: str) -> str:
        """Provides a simple rule-based response when AI is offline."""
        if "weakness" in prompt.lower() or "analyze" in prompt.lower():
            return "Rule-Based Advisor: The password contains common patterns or is too short. Try mixing uppercase, numbers, and special characters."
        if "improve" in prompt.lower() or "suggest" in prompt.lower():
            return "Rule-Based Advisor: Consider using a passphrase like 'Correct-Horse-Battery-Staple' or a random mix of characters."
        return "Rule-Based Advisor: AI models are currently offline. Please ensure your password is at least 12 characters long and uses a mix of characters."

    def explain_weakness(self, password: str) -> str:
        """Explains why a password is weak."""
        analysis = analyze_password_strength(password)
        if analysis['overall_score'] >= 80:
            return "This password is quite strong. No major weaknesses detected."
            
        prompt = f"""
        Act as a Senior Cybersecurity Engineer. Analyze this password and explain its vulnerabilities: '{password}'
        Current Strength Score: {analysis['overall_score']}/100.
        Known issues: {', '.join(analysis['suggestions'])}.
        Keep the explanation concise, educational, and easy to understand for a non-technical user.
        Do not output any introductory filler, just the analysis.
        """
        return self._generate_response(prompt)
        
    def suggest_improvement(self, password: str) -> str:
        """Suggests improvements for a weak password while keeping it memorable."""
        prompt = f"""
        Act as a UI/UX-aware Security Architect. The user has this weak password: '{password}'.
        Suggest 3 stronger alternatives that are related or memorable, but cryptographically secure.
        Explain briefly why the new ones are better (e.g., using entropy, bypassing dictionary attacks).
        Format as a clean bulleted list.
        """
        return self._generate_response(prompt)

    def ask_general_question(self, question: str) -> str:
        """Handles general cybersecurity chat."""
        prompt = f"""
        You are an elite Cybersecurity AI Assistant. Answer the following question accurately and concisely:
        User Question: {question}
        """
        return self._generate_response(prompt)
