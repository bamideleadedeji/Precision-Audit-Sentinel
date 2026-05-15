import os
import smtplib
from email.message import EmailMessage
import io

class PrecisionForensicEngine:
    def __init__(self):
        self.target_email = "bamideleadedeji2000@gmail.com"
        # 2026 CBN REGULATORY LIMITS
        self.SMS_CAP = 4.00
        self.EFT_BELOW_5K = 0.00
        self.EFT_5K_TO_50K = 10.00

    def analyze_csv_data(self, csv_content):
        """
        This function simulates reading a real bank statement.
        It looks for: Date, Description, Amount, and the Fee charged.
        """
        recovery_leads = []
        total_recovery_found = 0
        
        # Simulated lines from a Bank CSV (Date, Desc, Amount, Bank_Fee)
        # In a real scenario, we would use 'import csv' to read an actual file.
        transactions = [
            {"date": "2026-05-10", "desc": "Transfer to Mom", "amt": 3000, "fee": 52.50}, # VIOLATION: Should be 0
            {"date": "2026-05-11", "desc": "SMS ALERT", "amt": 0, "fee": 15.00},        # VIOLATION: Cap is 4
            {"date": "2026-05-12", "desc": "Business Payment", "amt": 25000, "fee": 35.00} # VIOLATION: Cap is 10
        ]

        for tx in transactions:
            if tx['amt'] < 5000 and "Transfer" in tx['desc'] and tx['fee'] > self.EFT_BELOW_5K:
                overcharge = tx['fee'] - self.EFT_BELOW_5K
                recovery_leads.append(f"OVERCHARGE: {tx['desc']} on {tx['date']}. Recoverable: ₦{overcharge}")
                total_recovery_found += overcharge
            
            if "SMS" in tx['desc'] and tx['fee'] > self.SMS_CAP:
                overcharge = tx['fee'] - self.SMS_CAP
                recovery_leads.append(f"OVERCHARGE: SMS fee on {tx['date']}. Recoverable: ₦{overcharge}")
                total_recovery_found += overcharge

        return recovery_leads, total_recovery_found

    def send_forensic_report(self, leads, total):
        msg = EmailMessage()
        body = f" PRECISION AUDIT: BANK CHARGE RECOVERY REPORT\n"
        body += "="*50 + "\n"
        body += f"TOTAL RECOVERABLE FOUND: ₦{total}\n"
        body += f"YOUR 15% COMMISSION: ₦{total * 0.15}\n"
        body += "="*50 + "\n\n"
        body += "DETAILED FINDINGS:\n"
        body += "\n".join(leads)
        
        msg.set_content(body)
        msg['Subject'] = f" FORENSIC SUCCESS: ₦{total} Recovery Identified"
        msg['From'] = "Sentinel-Forensics"
        msg['To'] = self.target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            smtp.send_message(msg)

if __name__ == "__main__":
    engine = PrecisionForensicEngine()
    # We pass 'None' for now as we are using the simulated 'transactions' list
    findings, total_recovered = engine.analyze_csv_data(None)
    
    if total_recovered > 0:
        engine.send_forensic_report(findings, total_recovered)
