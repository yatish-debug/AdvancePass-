import math
import re
from zxcvbn import zxcvbn

def calculate_shannon_entropy(password: str) -> float:
    """Calculates Shannon entropy of the password."""
    if not password:
        return 0.0
    
    # Calculate character frequencies
    freq = {}
    for char in password:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
            
    # Calculate entropy
    entropy = 0.0
    length = len(password)
    for count in freq.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
        
    return entropy

def calculate_pool_size(password: str) -> int:
    """Estimates the character pool size used in the password."""
    pool = 0
    if re.search(r'[a-z]', password):
        pool += 26
    if re.search(r'[A-Z]', password):
        pool += 26
    if re.search(r'[0-9]', password):
        pool += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        pool += 32 # Approximation of special characters
    return pool if pool > 0 else 1

def analyze_password_strength(password: str) -> dict:
    """
    Comprehensive password analysis combining zxcvbn, NIST guidelines, and entropy.
    """
    if not password:
        return {"score": 0, "feedback": ["Password cannot be empty."]}
        
    # 1. zxcvbn analysis (Dictionary, keyboard patterns, crack time)
    z_result = zxcvbn(password)
    
    # 2. Shannon Entropy and Pool Entropy
    shannon_ent = calculate_shannon_entropy(password)
    pool_size = calculate_pool_size(password)
    pool_entropy = len(password) * math.log2(pool_size) if pool_size > 1 else 0
    
    # 3. NIST SP 800-63B checks
    nist_feedback = []
    if len(password) < 8:
        nist_feedback.append("NIST SP 800-63B recommends a minimum of 8 characters.")
    
    # 4. Overall Score Calculation (0-100)
    # Zxcvbn score is 0-4. Let's map it roughly to 0-80, and add up to 20 points for high entropy.
    base_score = z_result['score'] * 20
    entropy_bonus = min(20, (pool_entropy / 100) * 20)
    overall_score = min(100, int(base_score + entropy_bonus))
    
    # Risk Level
    if overall_score < 20:
        risk_level = "Critical"
    elif overall_score < 40:
        risk_level = "Weak"
    elif overall_score < 60:
        risk_level = "Moderate"
    elif overall_score < 80:
        risk_level = "Strong"
    else:
        risk_level = "Excellent"
        
    # Combine feedback
    suggestions = z_result['feedback']['suggestions'] + nist_feedback
    if z_result['feedback']['warning']:
        suggestions.insert(0, z_result['feedback']['warning'])
        
    if not suggestions and overall_score < 100:
        suggestions.append("Add more length and mix character types to improve strength.")

    return {
        "overall_score": overall_score,
        "shannon_entropy": round(shannon_ent, 2),
        "pool_entropy": round(pool_entropy, 2),
        "crack_time_seconds": z_result['crack_times_seconds']['offline_slow_hashing_1e4_per_second'],
        "crack_time_display": z_result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
        "risk_level": risk_level,
        "suggestions": suggestions,
        "zxcvbn_score": z_result['score']
    }
