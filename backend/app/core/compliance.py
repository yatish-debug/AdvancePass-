def check_nist_compliance(password: str, is_breached: bool, in_dictionary: bool) -> bool:
    """
    Checks against NIST SP 800-63B guidelines.
    - Minimum length of 8 characters.
    - Not found in breach databases.
    - Not a commonly used or expected password (dictionary check).
    - Composition rules (require_upper, etc.) are NOT explicitly required by NIST, 
      but length and breach status are critical.
    """
    if len(password) < 8:
        return False
    if is_breached:
        return False
    if in_dictionary:
        return False
    return True

def check_owasp_compliance(password: str, is_breached: bool) -> bool:
    """
    Checks against OWASP Password Storage Cheat Sheet.
    - Minimum length of 10-12 characters depending on the application context, we use 10.
    - Requires composition rules (which we assume true if entropy/score is high enough, 
      but OWASP strictly recommends checking for breaches and complexity).
    """
    if len(password) < 10:
        return False
    if is_breached:
        return False
    
    # Check basic composition (must have at least 2 character classes)
    classes = 0
    import re
    if re.search(r"[a-z]", password): classes += 1
    if re.search(r"[A-Z]", password): classes += 1
    if re.search(r"[0-9]", password): classes += 1
    if re.search(r"[!@#$%^&*()\\-_=+]", password): classes += 1
    
    if classes < 2:
        return False
        
    return True
