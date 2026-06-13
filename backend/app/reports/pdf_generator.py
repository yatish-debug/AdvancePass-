import io
from fpdf import FPDF
from backend.app.models.analysis import PasswordAnalysisResult

class AdvancePassPDF(FPDF):
    def header(self):
        # Logo or Title
        self.set_font("helvetica", "B", 18)
        self.set_text_color(41, 128, 185) # Blue theme
        self.cell(0, 10, "AdvancePass v5.0", border=0, ln=1, align="C")
        self.set_font("helvetica", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Enterprise Password Security & Audit Report", border=0, ln=1, align="C")
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_single_report(result: PasswordAnalysisResult) -> bytes:
    pdf = AdvancePassPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Single Password Analysis Report", ln=1, align="L")
    pdf.ln(2)
    
    # Security Level & Score
    pdf.set_font("helvetica", "B", 12)
    if result.security_level == "Critical" or result.security_level == "Very Weak":
        pdf.set_text_color(200, 0, 0)
    elif result.security_level == "Weak" or result.security_level == "Moderate":
        pdf.set_text_color(200, 150, 0)
    else:
        pdf.set_text_color(0, 150, 0)
        
    pdf.cell(0, 10, f"Security Score: {result.composite_score}/100 ({result.security_level})", ln=1)
    
    # Metrics Table
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "", 10)
    pdf.ln(5)
    pdf.cell(60, 8, "Entropy:", border=1)
    pdf.cell(0, 8, f"{result.entropy:.2f} bits", border=1, ln=1)
    
    pdf.cell(60, 8, "Crack Time:", border=1)
    pdf.cell(0, 8, f"{result.crack_time}", border=1, ln=1)
    
    pdf.cell(60, 8, "Possible Combinations:", border=1)
    pdf.cell(0, 8, f"{result.possible_combinations:.2e}", border=1, ln=1)
    
    pdf.cell(60, 8, "HIBP Breach Count:", border=1)
    pdf.cell(0, 8, f"{result.hibp_count} times", border=1, ln=1)
    
    pdf.cell(60, 8, "NIST SP 800-63B Compliant:", border=1)
    pdf.cell(0, 8, "Yes" if result.nist_compliance else "No", border=1, ln=1)
    
    pdf.cell(60, 8, "OWASP Compliant:", border=1)
    pdf.cell(0, 8, "Yes" if result.owasp_compliance else "No", border=1, ln=1)
    
    pdf.ln(5)
    
    # Deductions/Warnings
    if result.warnings or result.password_reuse_detected:
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(200, 0, 0)
        pdf.cell(0, 10, "Risk Factors Detected:", ln=1)
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(0, 0, 0)
        if result.password_reuse_detected:
            pdf.multi_cell(0, 6, "- Warning: You have used this password before. Avoid reusing old passwords.")
        for warn in result.warnings:
            pdf.multi_cell(0, 6, f"- {warn}")
        pdf.ln(5)
        
    # AI Advice
    if result.ai_advice:
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "AI Security Advice:", ln=1)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 6, result.ai_advice)
        
    return bytes(pdf.output())

def generate_chat_report(title: str, messages: list) -> bytes:
    """Generates a PDF report of a complete AI chat thread."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 51, 102)
    # Sanitize title
    safe_title = title.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(0, 10, f"AdvancePass AI Advisor - {safe_title}", ln=True, align='C')
    pdf.ln(5)
    
    # Iterate through messages
    for msg in messages:
        role = "User" if msg["role"] == "user" else "AI Advisor"
        content = msg["content"]
        
        # Determine styling based on role
        if role == "User":
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 102, 204) # Blue
            pdf.cell(0, 8, "User:", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(40, 40, 40)
        else:
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 153, 76) # Green
            pdf.cell(0, 8, "AI Advisor:", ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(0, 0, 0)
            
        # Clean markdown formatting roughly for PDF
        clean_content = content.replace("**", "").replace("`", "").replace("\n\n", "\n")
        
        # Sanitize for latin-1 encoding to prevent FPDF font crash
        safe_content = clean_content.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 6, safe_content)
        pdf.ln(4)
        
    return bytes(pdf.output())

def generate_overall_report(stats: list, logs: list) -> bytes:
    pdf = AdvancePassPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Organizational Audit Report", ln=1, align="L")
    pdf.ln(5)
    
    # Stats Summary
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Overall Security Distribution:", ln=1)
    pdf.set_font("helvetica", "", 10)
    
    for stat in stats:
        # stat is a tuple (strength, count)
        pdf.cell(60, 8, str(stat[0]), border=1)
        pdf.cell(0, 8, str(stat[1]), border=1, ln=1)
        
    pdf.ln(10)
    
    # Logs Table (last 100 for report)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Recent Audit Logs (Hashes):", ln=1)
    
    pdf.set_font("helvetica", "B", 9)
    pdf.cell(40, 8, "Timestamp", border=1)
    pdf.cell(25, 8, "Strength", border=1)
    pdf.cell(20, 8, "Entropy", border=1)
    pdf.cell(105, 8, "Password Hash Suffix", border=1, ln=1)
    
    pdf.set_font("helvetica", "", 8)
    for log in logs[:100]:
        ts = str(log.get('timestamp', 'N/A'))
        strength = str(log.get('strength', 'N/A'))
        entropy = f"{log.get('entropy', 0):.1f}"
        p_hash = str(log.get('password_hash', ''))[-20:] # Only show partial hash for safety
        
        pdf.cell(40, 8, ts, border=1)
        pdf.cell(25, 8, strength, border=1)
        pdf.cell(20, 8, entropy, border=1)
        pdf.cell(105, 8, f"...{p_hash}", border=1, ln=1)
        
    return bytes(pdf.output())
