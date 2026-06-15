import re

def analyze_hash(hash_str: str) -> dict:
    """Analyzes a hash string to identify its algorithm and security properties."""
    hash_str = hash_str.strip()
    length = len(hash_str)
    
    # Defaults
    algo = "Unknown"
    rating = "Low"
    explanation = "Could not identify the hash format."
    alternative = "Use Argon2id, bcrypt, or scrypt for passwords."
    
    if hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
        algo = "bcrypt"
        rating = "Strong"
        explanation = "bcrypt is a key derivation function based on the Blowfish cipher. It incorporates a salt and is designed to be slow, resisting brute-force attacks."
        alternative = "Consider Argon2id for new systems, but bcrypt is still widely acceptable."
    elif hash_str.startswith("$argon2"):
        algo = "Argon2"
        rating = "Excellent"
        explanation = "Argon2 is the winner of the Password Hashing Competition. It is designed to be memory-hard and CPU-hard."
        alternative = "None. Argon2id is the current state-of-the-art recommendation."
    elif hash_str.startswith("$scrypt$"):
        algo = "scrypt"
        rating = "Strong"
        explanation = "scrypt is a password-based key derivation function designed to be memory-hard to prevent large-scale custom hardware attacks."
        alternative = "Argon2 is slightly preferred for new systems."
    elif length == 32 and re.match(r'^[a-fA-F0-9]+$', hash_str):
        algo = "MD5"
        rating = "Critical"
        explanation = "MD5 is a cryptographically broken hash function. It is extremely vulnerable to collision attacks and extremely fast to brute force."
        alternative = "Argon2, bcrypt, or scrypt."
    elif length == 40 and re.match(r'^[a-fA-F0-9]+$', hash_str):
        algo = "SHA-1"
        rating = "Critical"
        explanation = "SHA-1 is cryptographically broken and vulnerable to collision attacks."
        alternative = "Argon2, bcrypt, or scrypt."
    elif length == 64 and re.match(r'^[a-fA-F0-9]+$', hash_str):
        algo = "SHA-256"
        rating = "Weak (for passwords)"
        explanation = "SHA-256 is secure for general hashing, but too fast for password hashing, making it vulnerable to brute-force if used without a slow KDF."
        alternative = "PBKDF2-HMAC-SHA256, bcrypt, or Argon2."
    elif length == 128 and re.match(r'^[a-fA-F0-9]+$', hash_str):
        algo = "SHA-512"
        rating = "Weak (for passwords)"
        explanation = "SHA-512 is secure for data integrity, but too fast for password hashing alone."
        alternative = "Argon2, bcrypt, or scrypt."
        
    return {
        "algorithm": algo,
        "security_rating": rating,
        "explanation": explanation,
        "recommended_alternative": alternative
    }
