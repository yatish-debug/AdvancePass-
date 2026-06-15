import secrets
import string
import random
import os

# A small fallback wordlist for XKCD passphrases. In production, load a larger one.
FALLBACK_WORDS = ["correct", "horse", "battery", "staple", "ocean", "mountain", "river", "forest", 
                  "cyber", "security", "vault", "shield", "dragon", "wizard", "magic", "sword",
                  "purple", "yellow", "orange", "blue", "green", "happy", "fast", "brave"]

def load_wordlist():
    """Loads a wordlist from data/words.txt or falls back to internal list."""
    words_path = os.path.join(os.path.dirname(__file__), "..", "data", "words.txt")
    if os.path.exists(words_path):
        with open(words_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    return FALLBACK_WORDS

def generate_standard_password(length: int = 16, use_upper: bool = True, use_lower: bool = True, 
                               use_digits: bool = True, use_special: bool = True) -> str:
    """Generates a standard random password."""
    pool = ""
    if use_lower: pool += string.ascii_lowercase
    if use_upper: pool += string.ascii_uppercase
    if use_digits: pool += string.digits
    if use_special: pool += string.punctuation
    
    if not pool:
        pool = string.ascii_letters + string.digits
        
    password = []
    # Ensure at least one of each required type
    if use_lower: password.append(secrets.choice(string.ascii_lowercase))
    if use_upper: password.append(secrets.choice(string.ascii_uppercase))
    if use_digits: password.append(secrets.choice(string.digits))
    if use_special: password.append(secrets.choice(string.punctuation))
    
    # Fill the rest
    while len(password) < length:
        password.append(secrets.choice(pool))
        
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

def generate_xkcd_passphrase(num_words: int = 4, separator: str = "-") -> str:
    """Generates an XKCD-style passphrase."""
    words = load_wordlist()
    return separator.join(secrets.choice(words) for _ in range(num_words))

def generate_pronounceable_password(length: int = 10) -> str:
    """Generates a pronounceable password (alternating vowels and consonants)."""
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    password = ""
    use_vowel = secrets.choice([True, False])
    for _ in range(length):
        if use_vowel:
            password += secrets.choice(vowels)
        else:
            password += secrets.choice(consonants)
        use_vowel = not use_vowel
    
    # Capitalize first letter and add a number at the end for basic compliance
    return password.capitalize() + secrets.choice(string.digits)

def generate_by_profile(profile: str) -> str:
    """Generates a password based on a preset profile."""
    profiles = {
        "Personal": lambda: generate_standard_password(12, True, True, True, False),
        "Banking": lambda: generate_standard_password(16, True, True, True, True),
        "Corporate": lambda: generate_standard_password(20, True, True, True, True),
        "Developer": lambda: generate_xkcd_passphrase(5, "_"),
        "High Security": lambda: generate_standard_password(32, True, True, True, True)
    }
    return profiles.get(profile, profiles["Personal"])()

def bulk_generate(count: int, generator_func, *args, **kwargs) -> list:
    """Generates multiple passwords in bulk."""
    return [generator_func(*args, **kwargs) for _ in range(count)]
