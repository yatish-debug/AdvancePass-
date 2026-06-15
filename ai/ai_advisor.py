from typing import List, Dict, Any

def generate_advice(score: int, entropy: float, hibp_count: int, pattern_reasons: List[str], is_reused: bool) -> str:
    """
    Generates AI-like security advice based on the metrics.
    In the future, this can be swapped with a real LLM call.
    """
    if hibp_count > 0:
        return f"CRITICAL RISK: Your password has been exposed in {hibp_count} known data breaches. It is highly vulnerable to credential stuffing attacks. You must change it immediately. Never use this password again."
        
    if is_reused:
        return "HIGH RISK: You are reusing a password you have previously used. If this password is ever compromised, all associated accounts will be at risk. Use a unique password for every service."
        
    if score < 40:
        advice = "Your password is Very Weak. "
        if pattern_reasons:
            advice += f"It was penalized because: {', '.join(pattern_reasons).lower()} "
        advice += "To significantly improve resistance against dictionary and hybrid attacks, replace common words with unrelated terms, increase length, and add symbol diversity."
        return advice
        
    if score < 60:
        advice = "Your password is Weak. "
        if pattern_reasons:
            advice += f"It contains predictable elements: {', '.join(pattern_reasons).lower()} "
        advice += "Consider using a passphrase consisting of 4-5 random, unrelated words."
        return advice
        
    if score < 80:
        advice = "Your password is Medium strength. "
        if pattern_reasons:
            advice += f"However, it still contains minor predictable elements: {', '.join(pattern_reasons).lower()} "
        advice += "It has sufficient length and entropy for basic use, but could be improved by increasing the length to 16+ characters."
        return advice
        
    return "Your password is Strong. It has excellent entropy, no known patterns, and has not been found in any known data breaches. Excellent job!"
