import pandas as pd
from collections import Counter
import re

def analyze_dataset(file_content: bytes, filename: str) -> dict:
    """Analyzes a leaked password dataset (text or CSV)."""
    try:
        content_str = file_content.decode('utf-8')
    except UnicodeDecodeError:
        content_str = file_content.decode('latin-1')
        
    lines = content_str.splitlines()
    passwords = []
    
    if filename.endswith('.csv'):
        import csv
        reader = csv.reader(lines)
        for row in reader:
            if row:
                passwords.append(row[0]) # Assume first column is password for simplicity
    else:
        passwords = [line.strip() for line in lines if line.strip()]
        
    total_passwords = len(passwords)
    if total_passwords == 0:
        return {"error": "Dataset is empty or invalid format."}
        
    # Analyze frequency patterns
    lengths = [len(p) for p in passwords]
    avg_length = sum(lengths) / total_passwords
    
    # Common words/patterns
    all_words = []
    for p in passwords:
        # Extract purely alphabetical chunks
        chunks = re.findall(r'[a-zA-Z]+', p)
        all_words.extend([c.lower() for c in chunks if len(c) > 3])
        
    word_freq = Counter(all_words).most_common(10)
    
    # Character type distribution
    has_upper = sum(1 for p in passwords if any(c.isupper() for c in p))
    has_number = sum(1 for p in passwords if any(c.isdigit() for c in p))
    has_special = sum(1 for p in passwords if any(not c.isalnum() for c in p))
    
    return {
        "total_passwords": total_passwords,
        "avg_length": round(avg_length, 2),
        "most_common_words": word_freq,
        "composition": {
            "has_uppercase": round((has_upper / total_passwords) * 100, 2),
            "has_numbers": round((has_number / total_passwords) * 100, 2),
            "has_special": round((has_special / total_passwords) * 100, 2)
        }
    }
