import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import LogEntry

def get_overall_metrics(db: Session):
    """Retrieves overall metrics for the dashboard."""
    total_analyzed = db.query(LogEntry).count()
    if total_analyzed == 0:
        return {"total": 0, "avg_score": 0, "weak_count": 0, "strong_count": 0}
        
    # Assuming strength is stored as a string or score. Let's assume score (0-100) or label.
    # In V6, strength will be the overall score.
    # For now, let's pull all and calculate.
    logs = db.query(LogEntry).all()
    try:
        avg_score = sum(float(log.strength) for log in logs if log.strength.replace('.', '', 1).isdigit()) / total_analyzed
    except Exception:
        avg_score = 0
        
    weak_count = sum(1 for log in logs if float(log.strength) < 40 if log.strength.replace('.', '', 1).isdigit())
    strong_count = sum(1 for log in logs if float(log.strength) >= 80 if log.strength.replace('.', '', 1).isdigit())
    
    return {
        "total": total_analyzed,
        "avg_score": round(avg_score, 2),
        "weak_count": weak_count,
        "strong_count": strong_count
    }

def get_entropy_distribution(db: Session):
    """Gets entropy distribution for histograms."""
    entropies = [log.entropy for log in db.query(LogEntry.entropy).all() if log.entropy is not None]
    return entropies

def get_recent_history(db: Session, limit: int = 10):
    """Retrieves recent analysis history."""
    return db.query(LogEntry).order_by(LogEntry.timestamp.desc()).limit(limit).all()

def detect_reuse_in_list(passwords: list) -> dict:
    """Detects reuse within a given list of passwords."""
    counts = {}
    for p in passwords:
        counts[p] = counts.get(p, 0) + 1
        
    reused = {p: c for p, c in counts.items() if c > 1}
    total_unique = len(counts)
    total_reused = sum(c for c in reused.values())
    
    return {
        "total_passwords": len(passwords),
        "unique_passwords": total_unique,
        "reused_count": total_reused,
        "reuse_percentage": round((total_reused / len(passwords)) * 100, 2) if passwords else 0,
        "reused_details": reused
    }
