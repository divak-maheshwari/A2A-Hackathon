# services/gmail_sender.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from utils.email_utils import create_raw_email

def send_email_using_gmail_api(token: str, recipient: str, subject: str, body: str):
    creds = Credentials(token)
    service = build("gmail", "v1", credentials=creds)

    message = {
        "raw": create_raw_email(recipient, subject, body),
    }

    sent = service.users().messages().send(userId="me", body=message).execute()
    return sent
