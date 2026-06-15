import csv
import json
import os
from typing import List, Dict, Any

def export_report_csv(data: Dict[str, Any], filename: str = "password_report") -> str:
    filepath = f"{filename}.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data.keys())
        
        # Handle lists in values (like suggestions)
        row = []
        for val in data.values():
            if isinstance(val, list):
                row.append("; ".join(val))
            else:
                row.append(val)
        writer.writerow(row)
    return filepath

def export_report_json(data: Dict[str, Any], filename: str = "password_report") -> str:
    filepath = f"{filename}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return filepath
