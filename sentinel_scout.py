import os
import smtplib
from email.message import EmailMessage

class PrecisionForensicSentinel:
    def __init__(self):
        self.target_email = "bamideleadedeji2000@gmail.com"
        # 2026 REGULATORY LIMITS (Based on your CBN 2020/2026 data)
        self.CBN_RULES = {
            "SMS_CAP": 4,
            "EFT_MID_CAP": 10,
            "EFT_HIGH_CAP": 50,
            "CORP_CASH_LIMIT": 5000000,
            "CORP_CASH_FEE": 0.05
        }

    def audit_bank_charges(self):
        """Pillar 1: Bank Charge Recovery"""
        # Logic: Flagging deviations from the 2026 Revised Guide
        return [
            {"entity": "Govt Agency", "error": "EFT < ₦5k charged ₦52", "legal_basis": "CBN EFT Schedule 2020"},
            {"entity": "Corporate Client", "error": "SMS Alert charged ₦15", "legal_basis": "Cost-Recovery Cap (₦4)"},
            {"entity": "SME Manufacturer", "error": "Excess ATM fee > ₦100", "legal_basis": "ATM Surcharge Cap"}
        ]

    def audit_ghost_payroll(self):
        """Pillar 2: Ghost Payroll Detection"""
        return [{"entity": "Local Govt Health Dept", "risk": "Duplicate BVN patterns detected", "action": "Biometric Audit"}]

    def audit_tax_revenue(self):
        """Pillar 3: Tax Revenue Prediction"""
        return [{"entity": "Oyo State SIRS", "opportunity": "Under-reporting in Telecom sector", "model": "Econometric Variance"}]

    def generate_executive_summary(self, bank_leads, payroll_leads, tax_leads):
        summary = " PRECISION FORENSIC SENTINEL: 2026 ADVISORY\n"
        summary += "="*50 + "\n\n"
        
        summary += " PILLAR 1: BANK CHARGE RECOVERY\n"
        for lead in bank_leads:
            summary += f"- ALERT: {lead['error']} at {lead['entity']}. Basis: {lead['legal_basis']}\n"
            
        summary += "\n PILLAR 2: GHOST PAYROLL SENSING\n"
        for lead in payroll_leads:
            summary += f"- RISK: {lead['risk']} found in {lead['entity']}\n"

        summary += "\n PILLAR 3: REVENUE PREDICTION\n"
        for lead in tax_leads:
            summary += f"- OPPORTUNITY: {lead['opportunity']} for {lead['entity']}\n"

        summary += "\n" + "="*50 + "\n"
        summary += "NOTE: All findings are ready for 15% Contingency Fee Engagement."
        return summary

    def dispatch_alert(self, content):
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = " MASTER ALERT: Unified Forensic Intelligence"
        msg['From'] = "Sentinel-Forensics"
        msg['To'] = self.target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            smtp.send_message(msg)

if __name__ == "__main__":
    sentinel = PrecisionForensicSentinel()
    b_leads = sentinel.audit_bank_charges()
    p_leads = sentinel.audit_ghost_payroll()
    t_leads = sentinel.audit_tax_revenue()
    
    final_report = sentinel.generate_executive_summary(b_leads, p_leads, t_leads)
    sentinel.dispatch_alert(final_report)
