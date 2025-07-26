# utils/email_utils.py
import base64
from email.mime.text import MIMEText

def create_raw_email(to: str, subject: str, body: str) -> str:
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return raw
