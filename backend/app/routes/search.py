from fastapi import APIRouter, Query
from app.services.conversation_service import ConversationService

router = APIRouter(tags=["Search"], prefix="/search")

@router.get("")
def search_conversations(
    sentiment: str = Query(None, description="Sentiment label: Positive, Neutral, Negative"),
    escalated: bool = Query(None, description="Escalation detected: true/false"),
    platform: str = Query(None, description="Platform: email, chat, phone, twitter"),
    keyword: str = Query(None, description="Keyword in messages"),
    limit: int = Query(100, ge=1, le=1000)
):
    conversations = ConversationService.search_conversations(
        sentiment=sentiment,
        escalated=escalated,
        platform=platform,
        keyword=keyword,
        limit=limit
    )
    return {"total": len(conversations), "conversations": [c.dict(by_alias=True, exclude_none=True) for c in conversations]}
