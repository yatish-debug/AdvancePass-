import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.services.password_analyzer import analyze_password

def test_validation_matrix():
    passwords = [
        "password",
        "12345678",
        "Pass@123",
        "Pass@1234",
        "Admin@123",
        "Welcome123!",
        "P@ssw0rd",
        "CorrectHorseBatteryStaple",
        "MyDog@Blue#River27"
    ]
    
    print("="*60)
    print(f"{'Password':<25} | {'Score':<5} | {'Level':<12} | {'HIBP':<7}")
    print("="*60)
    
    for pwd in passwords:
        try:
            res = analyze_password(pwd)
            print(f"{pwd:<25} | {res.composite_score:<5} | {res.security_level:<12} | {res.hibp_count:<7}")
            # Print any errors to ensure things didn't fail
            if res.errors:
                print(f"  [!] Errors: {res.errors}")
            if res.warnings:
                print(f"  [-] Warnings: {res.warnings}")
        except Exception as e:
            print(f"{pwd:<25} | CRASHED: {e}")
            
if __name__ == "__main__":
    test_validation_matrix()
