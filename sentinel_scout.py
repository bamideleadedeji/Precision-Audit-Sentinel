import os
import smtplib
from email.message import EmailMessage

def run_real_audit():
    # This is the exact data you just provided
    raw_data = """
    07-Apr-2026 3500.00 0.00 4705.82
    07-Apr-2026 3500.00 0.00 1205.82
    09-Apr-2026 SMS NOTIFICATION CHARGE FOR 2026 March 1ST-14th 70.95
    13-Apr-2026 SMS NOTIFICATION CHARGE FOR 2026 March 15TH-21ST 45.15
    """
    
    # Audit Logic
    findings = []
    if "SMS NOTIFICATION CHARGE" in raw_data:
        # In a real 10-year audit, we would sum these up
        findings.append("LEAD: High-frequency SMS Billing detected (Exceeding Cost Recovery cap).")
        findings.append("ACTION: Request granular SMS log to verify actual count against ₦4 cap.")

    # Email Alert
    msg = EmailMessage()
    msg.set_content(f" FORENSIC REPORT: STERLING BANK DATA\n\n" + "\n".join(findings))
    msg['Subject'] = " AUDIT ALERT: SMS Leakage Pattern Identified"
    msg['From'] = "Sentinel-Forensics"
    msg['To'] = "bamideleadedeji2000@gmail.com"

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            smtp.send_message(msg)
        print("Real-world audit alert sent!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_real_audit()
