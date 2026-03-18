"""Conversation upload and retrieval routes"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.schemas import ConversationIn, ConversationAnalysisResponse
from app.services.conversation_service import ConversationService
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Conversations"], prefix="/conversations")


def _convert_objectid(obj):
    """Convert ObjectId to string in dictionaries for JSON serialization"""
    if isinstance(obj, dict):
        return {k: _convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_objectid(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj


@router.post("/upload-thread", response_model=ConversationAnalysisResponse)
async def upload_thread(conversation: ConversationIn):
    """
    Upload and analyze a customer support conversation thread
    
    Args:
        conversation: ConversationIn with thread_id, platform, and messages
        
    Returns:
        ConversationAnalysisResponse with sentiment analysis and escalation detection
    """
    if not conversation.messages:
        raise HTTPException(status_code=400, detail="Conversation must have at least one message")
    
    try:
        result = ConversationService.process_conversation(conversation, use_vader=True)
        return result
    except Exception as e:
        logger.error(f"Error processing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{thread_id}")
async def get_conversation(thread_id: str):
    """Get a specific conversation by thread_id"""
    try:
        conversation = ConversationService.get_conversation(thread_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        data = conversation.dict(by_alias=True, exclude_none=True)
        return _convert_objectid(data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def get_conversations(limit: int = Query(100, ge=1, le=1000)):
    """Get all conversations with optional limit"""
    try:
        conversations = ConversationService.get_all_conversations(limit=limit)
        result = {
            "total": len(conversations),
            "conversations": [_convert_objectid(c.dict(by_alias=True, exclude_none=True)) for c in conversations]
        }
        return result
    except Exception as e:
        logger.error(f"Error retrieving conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{thread_id}/sentiment-trajectory")
async def get_sentiment_trajectory(thread_id: str):
    """Get sentiment trajectory for a conversation"""
    try:
        trajectory = ConversationService.get_sentiment_trajectory(thread_id)
        if trajectory is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"thread_id": thread_id, "trajectory": trajectory}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving sentiment trajectory: {e}")
        raise HTTPException(status_code=500, detail=str(e))
