from pydantic import BaseModel, Field
from typing import List

class PasswordAnalysisResult(BaseModel):
    password: str = ""
    composite_score: int = 0
    security_level: str = "Critical"
    entropy: float = 0.0
    possible_combinations: float = 0.0
    crack_time: str = ""
    suggestions: List[str] = Field(default_factory=list)
    dictionary_match: bool = False
    dictionary_word: str = ""
    keyboard_pattern_detected: bool = False
    sequential_pattern_detected: bool = False
    repeated_pattern_detected: bool = False
    password_reuse_detected: bool = False
    hibp_checked: bool = False
    hibp_count: int = 0
    hibp_breached: bool = False
    breach_status: str = "Not Checked"
    nist_compliance: int = 0
    owasp_compliance: int = 0
    ai_advice: str = ""
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
