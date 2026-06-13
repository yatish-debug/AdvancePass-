import re
import math
from backend.app.models.analysis import PasswordAnalysisResult
from backend.app.core.pattern_detector import analyze_patterns, detect_dictionary_mutations, check_keyboard_patterns, check_sequential_patterns, check_repeated_characters
from backend.app.core.breach_checker import check_hibp
from backend.app.core.compliance import check_nist_compliance, check_owasp_compliance
from backend.app.ai.ai_advisor import generate_advice
from backend.app.database.db_manager import check_password_reuse

def _calculate_entropy(pwd: str) -> float:
    pool = 0
    if re.search(r"[a-z]", pwd): pool += 26
    if re.search(r"[A-Z]", pwd): pool += 26
    if re.search(r"[0-9]", pwd): pool += 10
    if re.search(r"[!@#$%^&*()\\-_=+]", pwd): pool += 14
    if pool == 0:
        return 0.0
    return len(pwd) * math.log2(pool)

def _format_time(seconds: float) -> str:
    if seconds < 60: return f"{seconds:.2f} seconds"
    elif seconds < 3600: return f"{seconds/60:.2f} minutes"
    elif seconds < 86400: return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000: return f"{seconds/86400:.2f} days"
    else: return f"{seconds/31536000:.2f} years"

def analyze_password(password: str) -> PasswordAnalysisResult:
    result = PasswordAnalysisResult(password=password)
    if not password:
        result.errors.append("Empty password provided.")
        return result

    # 1. Entropy & Base Score
    result.entropy = _calculate_entropy(password)
    result.possible_combinations = 2 ** result.entropy
    result.crack_time = _format_time(result.possible_combinations / 1e9)
    base_score = min(100, int(result.entropy))

    # 2. Database Reuse
    try:
        result.password_reuse_detected = check_password_reuse(password)
    except Exception as e:
        result.errors.append(f"Database error during reuse check: {e}")

    # 3. Pattern Detection (Safe Execution)
    try:
        result.dictionary_match = detect_dictionary_mutations(password)
        result.keyboard_pattern_detected = check_keyboard_patterns(password)
        result.sequential_pattern_detected = check_sequential_patterns(password)
        result.repeated_pattern_detected = check_repeated_characters(password)
        
        pattern_reasons, pattern_deduction = analyze_patterns(password)
        result.warnings.extend(pattern_reasons)
    except Exception as e:
        pattern_deduction = 0
        result.errors.append(f"Pattern detection error: {e}")

    # 4. HIBP Integration (Safe Execution)
    try:
        result.hibp_count = check_hibp(password)
        result.hibp_checked = True
        if result.hibp_count > 0:
            result.hibp_breached = True
            result.breach_status = "Breached"
        else:
            result.hibp_breached = False
            result.breach_status = "No Breach Found"
    except Exception as e:
        result.hibp_checked = False
        result.hibp_count = 0
        result.hibp_breached = False
        result.breach_status = "API Unavailable"
        result.errors.append(f"HIBP API error: {e}")

    # 5. Composite Score Calculation
    score = base_score - pattern_deduction
    score = max(0, score)
    
    if result.hibp_breached or result.dictionary_match or result.password_reuse_detected:
        score = min(score, 20) # Hard cap for critical vulnerabilities

    result.composite_score = score

    # Security Level Mapping
    if score <= 20: result.security_level = "Critical"
    elif score <= 40: result.security_level = "Very Weak"
    elif score <= 60: result.security_level = "Weak"
    elif score <= 80: result.security_level = "Moderate"
    else: result.security_level = "Strong"

    # 6. Compliance (Safe Execution)
    try:
        result.nist_compliance = 1 if check_nist_compliance(password, result.hibp_breached, result.dictionary_match) else 0
        result.owasp_compliance = 1 if check_owasp_compliance(password, result.hibp_breached) else 0
    except Exception as e:
        result.errors.append(f"Compliance check error: {e}")

    # 7. AI Advisor (Safe Execution)
    try:
        result.ai_advice = generate_advice(
            score, result.entropy, result.hibp_count, result.warnings, result.password_reuse_detected
        )
    except Exception as e:
        result.ai_advice = ""
        result.warnings.append("AI Advisor temporarily unavailable.")
        result.errors.append(f"AI Advisor error: {e}")

    return result
