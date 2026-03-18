from fastapi import APIRouter, Response
from app.services.conversation_service import ConversationService
import csv
import io

router = APIRouter(tags=["Export"], prefix="/export")

@router.get("/conversations/csv")
def export_conversations_csv():
    conversations = ConversationService.get_all_conversations(limit=1000)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["thread_id", "platform", "created_at", "sentiment", "escalation", "final_outcome"])
    for conv in conversations:
        writer.writerow([
            conv.thread_id,
            conv.platform,
            conv.created_at,
            conv.overall_sentiment_label,
            conv.escalation_detected,
            conv.final_outcome
        ])
    csv_data = output.getvalue()
    return Response(content=csv_data, media_type="text/csv")
