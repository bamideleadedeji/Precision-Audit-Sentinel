import os
import smtplib
from email.message import EmailMessage

# --- THE AUDIT LOGIC ---
def scout_for_leads():
    # In a real scenario, this would scrape a news API or RSS feed
    # For now, we simulate finding a high-value lead
    leads_found = ["Dangote Refinery New Procurement Tender", "Federal Ministry of Works Iron Rod Supply"]
    return leads_found

# --- THE ALERT LOGIC ---
def send_alert(leads):
    msg = EmailMessage()
    msg.set_content(f"Bamidele, the Sentinel has found new leads:\n\n" + "\n".join(leads))
    msg['Subject'] = "🚨 AUDIT ALERT: New Procurement Leads Identified"
    msg['From'] = "Your-Sentinel-System"
    msg['To'] = "bamideleadedeji2000@gmail.com"

    # This uses GitHub Secrets to keep your password safe
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        smtp.send_message(msg)

if __name__ == "__main__":
    new_leads = scout_for_leads()
    if new_leads:
        send_alert(new_leads)