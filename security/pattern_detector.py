import re
import os
from typing import Tuple, List

# Build a simple builtin list to avoid external dependency block, but allow loading
BUILTIN_DICTIONARY = {"password", "admin", "welcome", "123456", "qwerty", "letmein", "sunshine", "monkey", "dragon"}

def load_local_dictionaries() -> set:
    words = set(BUILTIN_DICTIONARY)
    datasets_dir = os.path.join(os.path.dirname(__file__), '..', 'datasets')
    if os.path.exists(datasets_dir):
        for filename in os.path.isfile(datasets_dir):
            if filename.endswith(".txt"):
                try:
                    with open(os.path.join(datasets_dir, filename), "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            words.add(line.strip().lower())
                except Exception:
                    pass
    return words

COMMON_WORDS = load_local_dictionaries()

def unleet(password: str) -> str:
    """Replaces common leetspeak characters with normal letters."""
    leet_map = {
        '@': 'a', '4': 'a',
        '0': 'o',
        '1': 'i', '!': 'i',
        '3': 'e',
        '5': 's', '$': 's',
        '7': 't'
    }
    unleeted = ""
    for char in password.lower():
        unleeted += leet_map.get(char, char)
    return unleeted

def detect_dictionary_mutations(password: str) -> bool:
    """Checks if password is a dictionary word with a common suffix/prefix stripped."""
    pwd_lower = password.lower()
    
    # 1. Check direct dictionary match
    if pwd_lower in COMMON_WORDS:
        return True
        
    # 2. Check unleeted direct match
    if unleet(pwd_lower) in COMMON_WORDS:
        return True
        
    # 3. Strip suffix first, then check
    stripped_suffix = re.sub(r'(\d+|[!@#$%^&*]+)$', '', pwd_lower)
    if stripped_suffix:
        if stripped_suffix in COMMON_WORDS or unleet(stripped_suffix) in COMMON_WORDS:
            return True
            
    # 4. Strip prefix first, then check
    stripped_prefix = re.sub(r'^(\d+|[!@#$%^&*]+)', '', pwd_lower)
    if stripped_prefix:
        if stripped_prefix in COMMON_WORDS or unleet(stripped_prefix) in COMMON_WORDS:
            return True
            
    return False

def check_keyboard_patterns(password: str) -> bool:
    """Checks for common keyboard walking patterns."""
    patterns = [
        "qwertyuiop", "asdfghjkl", "zxcvbnm",
        "1234567890", "qazwsxedc"
    ]
    pwd_lower = password.lower()
    for p in patterns:
        if pwd_lower in p or p in pwd_lower:
            # We want to match at least length 4 or 5 sequences
            return True
            
    # Check substrings of length >= 5
    for p in patterns:
        for i in range(len(p) - 4):
            sub = p[i:i+5]
            if sub in pwd_lower:
                return True
                
    # Also check reverse
    pwd_lower_rev = pwd_lower[::-1]
    for p in patterns:
        for i in range(len(p) - 4):
            sub = p[i:i+5]
            if sub in pwd_lower_rev:
                return True
                
    return False

def check_sequential_patterns(password: str) -> bool:
    """Checks for sequential abcde or 12345."""
    pwd_lower = password.lower()
    
    # Check alphabet sequence
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(alphabet) - 4):
        if alphabet[i:i+5] in pwd_lower:
            return True
    # Reverse
    for i in range(len(alphabet) - 4):
        if alphabet[i:i+5][::-1] in pwd_lower:
            return True
            
    return False

def check_repeated_characters(password: str) -> bool:
    """Checks for aaaaa, 111111 or repeating sequences like 121212."""
    if re.search(r'(.)\1{3,}', password): # 4 or more identical chars
        return True
    if re.search(r'(.{2,})\1{2,}', password): # Sequence repeated 3 or more times e.g. 121212
        return True
    return False

def analyze_patterns(password: str) -> Tuple[List[str], int]:
    """
    Returns a list of reasons why the password has patterns and the suggested score deduction.
    """
    reasons = []
    deduction = 0
    
    if detect_dictionary_mutations(password):
        reasons.append("Contains dictionary word or simple mutation (e.g., leetspeak or common suffixes).")
        deduction += 30
        
    if check_keyboard_patterns(password):
        reasons.append("Contains common keyboard pattern (e.g., qwerty).")
        deduction += 20
        
    if check_sequential_patterns(password):
        reasons.append("Contains sequential characters (e.g., abcde, 12345).")
        deduction += 15
        
    if check_repeated_characters(password):
        reasons.append("Contains repeated characters or sequences.")
        deduction += 15
        
    return reasons, deduction
