import random
import string

def generate_strong_password(length: int = 12, include_upper: bool = True, 
                             include_lower: bool = True, include_digits: bool = True, 
                             include_symbols: bool = True, exclude_ambiguous: bool = False) -> str:
    if length < 12:
        length = 12
        
    characters = ""
    if include_lower:
        characters += string.ascii_lowercase
    if include_upper:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += "!@#$%^&*()-_+="
        
    if exclude_ambiguous:
        ambiguous = "0OIl1"
        characters = ''.join(c for c in characters if c not in ambiguous)

    if not characters:
        characters = string.ascii_letters + string.digits + "!@#$%^&*()-_+="
        
    return ''.join(random.choice(characters) for _ in range(length))

def generate_memorable_password(words_count: int = 4, separator: str = "-") -> str:
    # A simple memorable password generator for now (expandable later)
    # Using a small built-in list to avoid external dependencies for the MVP
    word_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", 
                 "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", 
                 "strawberry", "tangerine", "watermelon", "blueberry", "blackberry", "cranberry"]
    
    selected_words = [random.choice(word_list) for _ in range(words_count)]
    return separator.join(selected_words)

def generate_passphrase(words_count: int = 4, separator: str = " ") -> str:
    return generate_memorable_password(words_count, separator)
