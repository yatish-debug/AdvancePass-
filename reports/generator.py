import os
import csv
import json
from fpdf import FPDF
from docx import Document

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "exports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def _get_filename(base_name: str, ext: str) -> str:
    return os.path.join(REPORTS_DIR, f"{base_name}.{ext}")

def generate_csv_report(data: list, base_name: str = "security_report") -> str:
    """Generates a CSV report from a list of dictionaries."""
    if not data: return ""
    filepath = _get_filename(base_name, "csv")
    keys = data[0].keys()
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    return filepath

def generate_json_report(data: list, base_name: str = "security_report") -> str:
    """Generates a JSON report."""
    filepath = _get_filename(base_name, "json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return filepath

def generate_pdf_report(data: list, base_name: str = "security_report") -> str:
    """Generates a professional PDF report."""
    filepath = _get_filename(base_name, "pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AdvancePass V6.0 Security Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    for item in data:
        for k, v in item.items():
            pdf.cell(200, 8, txt=f"{k}: {v}", ln=True)
        pdf.ln(5)
        
    pdf.output(filepath)
    return filepath

def generate_docx_report(data: list, base_name: str = "security_report") -> str:
    """Generates a DOCX report."""
    filepath = _get_filename(base_name, "docx")
    doc = Document()
    doc.add_heading('AdvancePass V6.0 Security Report', 0)
    
    for item in data:
        p = doc.add_paragraph()
        for k, v in item.items():
            p.add_run(f"{k}: ").bold = True
            p.add_run(f"{v}\n")
            
    doc.save(filepath)
    return filepath

def generate_dashboard_pdf(metrics: dict, chart1_path: str = None, chart2_path: str = None, base_name: str = "dashboard_report") -> str:
    """Generates a PDF report for the Dashboard metrics with charts."""
    filepath = _get_filename(base_name, "pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AdvancePass V6.0 Enterprise Dashboard Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Summary Metrics:", ln=True)
    pdf.ln(5)
    
    def add_metric_row(label, value):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(80, 8, txt=label, ln=False)
        pdf.set_font("Arial", size=12)
        pdf.cell(100, 8, txt=str(value), ln=True)

    add_metric_row("Total Passwords Analyzed:", metrics.get("total", 0))
    add_metric_row("Average Security Score:", f"{metrics.get('avg_score', 0)}/100")
    add_metric_row("Weak Passwords Detected:", metrics.get("weak_count", 0))
    add_metric_row("Moderate Passwords:", metrics.get("total", 0) - metrics.get("weak_count", 0) - metrics.get("strong_count", 0))
    add_metric_row("Strong Passwords:", metrics.get("strong_count", 0))

    pdf.ln(10)
    
    # Embed charts
    y_pos = pdf.get_y()
    if chart1_path and os.path.exists(chart1_path):
        pdf.cell(200, 10, txt="Strength Distribution", ln=True)
        pdf.image(chart1_path, x=10, y=pdf.get_y(), w=90)
        
    if chart2_path and os.path.exists(chart2_path):
        pdf.set_y(y_pos)
        pdf.cell(200, 10, txt="Entropy Distribution", ln=True, align='R')
        pdf.image(chart2_path, x=110, y=pdf.get_y(), w=90)

    pdf.output(filepath)
    return filepath

