import smtplib
from email.mime.text import MIMEText
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for sending escalation notifications"""

    @staticmethod
    def send_email_notification(to_email: str, subject: str, body: str, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str) -> Optional[str]:
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = to_email

            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.sendmail(smtp_user, [to_email], msg.as_string())
            logger.info(f"Notification email sent to {to_email}")
            return None
        except Exception as e:
            logger.error(f"Failed to send notification email: {e}")
            return str(e)

    @staticmethod
    def send_webhook_notification(webhook_url: str, payload: dict) -> Optional[str]:
        import requests
        try:
            response = requests.post(webhook_url, json=payload)
            logger.info(f"Webhook notification sent: {response.status_code}")
            if response.status_code != 200:
                return f"Webhook failed: {response.text}"
            return None
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return str(e)
