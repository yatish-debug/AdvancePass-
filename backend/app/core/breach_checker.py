import hashlib
import requests

def check_hibp(password: str) -> int:
    """
    Checks the Have I Been Pwned API using k-Anonymity (SHA-1).
    Returns the number of times the password has been breached.
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    return int(count)
        return 0
    except Exception as e:
        # In case of network error, return 0 or log warning
        print(f"Warning: HIBP check failed - {e}")
        return 0
