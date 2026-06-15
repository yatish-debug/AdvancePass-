import os
import hashlib

BREACH_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "breached_hashes.txt")

def check_breach(password: str) -> dict:
    """
    Checks if a password is in the local breached database.
    We simulate checking an offline SHA-1 hash list (similar to HIBP's offline list).
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    breached = False
    count = 0
    
    if os.path.exists(BREACH_DATA_FILE):
        # The file is expected to be sorted or we just grep it (in a real app, use a binary search or bloom filter)
        with open(BREACH_DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Expected format: HASH_SUFFIX:COUNT
                if line.startswith(sha1_hash):
                    breached = True
                    parts = line.split(':')
                    if len(parts) > 1:
                        count = int(parts[1])
                    else:
                        count = 1
                    break
    
    # Fallback/Demo: check against some common bad passwords if file is missing
    if not os.path.exists(BREACH_DATA_FILE) and password in ['password', '123456', 'qwerty']:
        breached = True
        count = 1000000

    severity = "High" if count > 1000 else "Medium" if count > 0 else "Low"

    return {
        "breached": breached,
        "count": count,
        "severity": severity if breached else "None",
        "recommendation": "Change this password immediately across all your accounts." if breached else "No known breaches found in local database."
    }
