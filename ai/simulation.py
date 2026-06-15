import string
import math

def simulate_dictionary_attack(password: str) -> dict:
    """Simulates a dictionary attack."""
    # Assuming standard dictionary size is ~1 million words.
    # We estimate based on word splits (very rudimentary for demonstration).
    is_pure_alpha = password.isalpha()
    time_taken = 0.001 if is_pure_alpha and len(password) < 10 else 99999
    success = time_taken < 1.0
    return {
        "attack_type": "Dictionary Attack",
        "success": success,
        "estimated_time_seconds": time_taken,
        "description": "Checks password against a precompiled list of common words. " + 
                       ("Vulnerable because it appears to be a simple word." if success else "Resistant to simple word lists.")
    }

def simulate_bruteforce_attack(password: str, speed_hashes_per_sec: int = 100_000_000_000) -> dict:
    """Simulates a brute-force attack."""
    # Pool size estimation
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 32
    if pool == 0: pool = 1
    
    combinations = pool ** len(password)
    seconds = combinations / speed_hashes_per_sec
    success = seconds < (3600 * 24) # Success if broken in < 1 day
    
    return {
        "attack_type": "Brute-Force Attack",
        "success": success,
        "estimated_time_seconds": seconds,
        "description": f"Trying every possible combination of characters. Assuming {speed_hashes_per_sec:,} hashes/sec."
    }

def simulate_mutation_attack(password: str) -> dict:
    """Demonstrates common attacker mutation techniques."""
    mutations = []
    
    # 1. Leetspeak
    leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
    leet_pass = "".join(leet_map.get(c.lower(), c) for c in password)
    if leet_pass != password:
        mutations.append(f"Leetspeak: {leet_pass}")
        
    # 2. Append years/numbers
    mutations.append(f"Append Year: {password}2026")
    mutations.append(f"Append Number: {password}123")
    
    # 3. Capitalize first letter + append symbol
    if password.islower():
        mutations.append(f"Cap+Symbol: {password.capitalize()}!")
        
    return {
        "attack_type": "Mutation / Rule-Based Attack",
        "success": True, # It's just generating list
        "mutations_generated": mutations,
        "description": "Applies common rules (like adding '123' or '!' to the end) to base dictionary words."
    }
