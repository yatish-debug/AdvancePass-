import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.services.password_service import PasswordService
from backend.app.reports.pdf_generator import generate_single_report

st.title("🛡️ Password Checker")

password = st.text_input("Enter Password to Analyze:", type="password")

if st.button("Check Password"):
    if password:
        with st.spinner("Analyzing password metrics and checking breach databases..."):
            try:
                result = PasswordService.check_password(password)
                
                # If there are internal errors but the model returned, show a warning
                if getattr(result, 'errors', []):
                    st.warning("⚠ Password analysis could not be fully completed. Some online services are temporarily unavailable. Basic analysis results are still displayed.")
                    for err in result.errors:
                        # Log to console, don't show full traceback to user
                        print(f"Backend Error: {err}")

                score = result.composite_score
                strength = result.security_level
                
                # Color code based on strength
                progress_class = "progress-strong"
                if score <= 20: progress_class = "progress-very-weak"
                elif score <= 40: progress_class = "progress-very-weak"
                elif score <= 60: progress_class = "progress-weak"
                elif score <= 80: progress_class = "progress-medium"
                
                st.markdown(f'<div class="{progress_class}">', unsafe_allow_html=True)
                st.progress(score / 100) # Progress bar expects 0.0 - 1.0
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown(f"### Composite Security Score: **{score}/100** ({strength})")
                
                # Core Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Entropy", f"{result.entropy:.2f} bits")
                col2.metric("Crack Time", result.crack_time)
                col3.metric("Possible Combinations", f"{result.possible_combinations:.2e}")
                
                st.markdown("---")
                
                # Breach & Risk Status
                col_breach, col_nist, col_owasp = st.columns(3)
                with col_breach:
                    if result.hibp_breached:
                        st.error(f"🚨 BREACHED ({result.hibp_count} times)")
                    elif not result.hibp_checked:
                        st.warning("⚠️ Breach Check Unavailable")
                    else:
                        st.success("✅ Secure (No known breaches)")
                
                with col_nist:
                    if result.nist_compliance == 1:
                        st.success("✅ NIST SP 800-63B Compliant")
                    else:
                        st.error("❌ Fails NIST Guidelines")
                        
                with col_owasp:
                    if result.owasp_compliance == 1:
                        st.success("✅ OWASP Compliant")
                    else:
                        st.error("❌ Fails OWASP Guidelines")

                # Deductions & Warnings
                if result.warnings or result.password_reuse_detected:
                    st.markdown("### Risk Factors Detected")
                    if result.password_reuse_detected:
                        st.warning("⚠️ You have used this password before. Avoid reusing old passwords.")
                    for reason in result.warnings:
                        st.warning(f"⚠️ {reason}")
                        
                # AI Advice
                if result.ai_advice:
                    st.markdown("### 🤖 AI Security Advice")
                    st.info(result.ai_advice)

                st.markdown("---")
                st.markdown("### 📄 Export Options")
                
                pdf_bytes = generate_single_report(result)
                st.download_button(
                    label="📥 Download Professional Report (PDF)",
                    data=pdf_bytes,
                    file_name="password_security_report.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                # Catch-all for catastrophic frontend/backend failures
                st.error("⚠ An unexpected error occurred during password analysis. Please try again later.")
                print(f"Catastrophic Error: {e}")
            
    else:
        st.error("Please enter a password.")
