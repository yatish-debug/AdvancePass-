from backend.app.services.password_analyzer import analyze_password
from backend.app.core.generator import generate_strong_password, generate_memorable_password, generate_passphrase
from backend.app.database.db_manager import log_to_db, get_statistics, get_all_logs, clear_history
from backend.app.reports.exporter import export_report_csv, export_report_json
from backend.app.models.analysis import PasswordAnalysisResult

class PasswordService:
    @staticmethod
    def check_password(password: str) -> PasswordAnalysisResult:
        # Evaluate with the new unified Pydantic model
        result = analyze_password(password)
        
        # Log to DB
        log_to_db(password, result.security_level, result.entropy, result.crack_time)
            
        return result

    @staticmethod
    def generate_random_password(length: int, include_upper: bool, include_lower: bool, 
                                 include_digits: bool, include_symbols: bool, exclude_ambiguous: bool) -> str:
        return generate_strong_password(length, include_upper, include_lower, include_digits, include_symbols, exclude_ambiguous)

    @staticmethod
    def generate_memorable(words: int, separator: str) -> str:
        return generate_memorable_password(words, separator)
        
    @staticmethod
    def get_stats() -> list:
        return get_statistics()
        
    @staticmethod
    def get_history() -> list:
        return get_all_logs()

    @staticmethod
    def clear_database():
        clear_history()
