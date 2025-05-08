# backend_api/app/routers/utils_postmark.py

import os
import requests
from Contactmessage import ContactMessage

POSTMARK_API_KEY = os.getenv("POSTMARK_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")  # Postmark에서 인증한 발신자 이메일
TO_EMAIL = os.getenv("TO_EMAIL_CONTACT_POSTMARK")      # 수신자 이메일
MESSAGE_STREAM = os.getenv("POSTMARK_MESSAGE_STREAM", "outbound")  # 기본 메시지 스트림

def convert_text_to_html(text: str) -> str:
    """텍스트 개행을 <br>로 변환"""
    return text.replace("\n", "<br>")

def send_email_via_postmark(message: ContactMessage):
    if not POSTMARK_API_KEY or not FROM_EMAIL or not TO_EMAIL:
        raise ValueError("Missing POSTMARK_API_KEY, FROM_EMAIL, or TO_EMAIL in environment variables")

    subject = f"[Portfolio Contact] {message.subject}"
    html_body = f"""
    <strong>From:</strong> {message.name} ({message.email})<br>
    <strong>Message:</strong><br>
    {convert_text_to_html(message.message)}
    """

    url = "https://api.postmarkapp.com/email"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": POSTMARK_API_KEY
    }

    data = {
        "From": FROM_EMAIL,
        "To": TO_EMAIL,
        "Subject": subject,
        "HtmlBody": html_body,
        "TextBody": message.message,
        "MessageStream": MESSAGE_STREAM
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Postmark API error: {str(e)}")
