import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.services.password_service import PasswordService

def test():
    test_cases = [
        "P@ssw0rd123", # Leetspeak + mutation + HIBP
        "qwerty99",    # Keyboard pattern + mutation
        "super_secure_random_phrase_2024!", # Strong
        "123456"       # HIBP + sequential
    ]
    
    for pwd in test_cases:
        res = PasswordService.check_password(pwd)
        print(f"\nPassword: {pwd}")
        print(f"Score: {res['score']}")
        print(f"Strength: {res['strength']}")
        print(f"HIBP Count: {res['hibp_count']}")
        print(f"NIST Compliant: {res['nist_compliant']}")
        print(f"OWASP Compliant: {res['owasp_compliant']}")
        print(f"Deductions: {res['deductions']}")
        
if __name__ == "__main__":
    test()
