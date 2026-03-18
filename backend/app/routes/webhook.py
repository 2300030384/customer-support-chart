from fastapi import APIRouter, Request
from app.services.notification_service import NotificationService

router = APIRouter()

@router.post("/webhook/escalation")
def receive_escalation_webhook(request: Request):
    payload = request.json()
    # Example: log or process webhook payload
    # You can trigger further actions here
    return {"status": "received", "payload": payload}

@router.post("/webhook/test")
def test_webhook():
    # Example: send a test webhook notification
    NotificationService.send_webhook_notification(
        webhook_url="https://your-webhook-url.com/notify",
        payload={"test": "webhook", "status": "success"}
    )
    return {"status": "webhook sent"}
