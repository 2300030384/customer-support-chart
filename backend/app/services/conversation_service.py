"""
Conversation Service
Orchestrates sentiment analysis, escalation detection, and database operations
"""
from typing import List, Optional
from datetime import datetime
from pymongo import DESCENDING
from app.database.connection import get_database
from app.models.schemas import (
    ConversationIn, Conversation, Message, ConversationAnalysisResponse,
    SentimentAnalysisResult
)
from app.services.sentiment_analyzer import analyze_turn, analyze_conversation, calculate_overall_sentiment
from app.services.escalation_detector import (
    detect_escalation_per_message, detect_overall_escalation, contains_trigger_words
)
import logging

logger = logging.getLogger(__name__)


class ConversationService:
    """Service for conversation processing and storage"""
    
    @staticmethod
    def process_conversation(conversation_in: ConversationIn, use_vader: bool = True) -> ConversationAnalysisResponse:
        """
        Process a conversation:
        1. Analyze sentiment for each message
        2. Detect escalation
        3. Store in MongoDB
        
        Args:
            conversation_in: Input conversation data
            use_vader: Use VADER if True, else HuggingFace
            
        Returns:
            ConversationAnalysisResponse with analysis results
        """
        db = get_database()
        texts = [msg.text for msg in conversation_in.messages]
        speakers = [msg.speaker for msg in conversation_in.messages]
        
        # Analyze sentiment for each turn
        sentiment_scores = []
        processed_messages = []
        
        for message_in in conversation_in.messages:
            score, label, confidence = analyze_turn(message_in.text, use_vader=use_vader)
            sentiment_scores.append(score)
            
            # Create enriched message
            message = Message(
                speaker=message_in.speaker,
                text=message_in.text,
                timestamp=message_in.timestamp,
                sentiment_score=score,
                sentiment_label=label,
                escalation_flag=False
            )
            processed_messages.append(message)
        
        # Detect escalation per message
        escalation_flags, _ = detect_escalation_per_message(sentiment_scores, texts, [str(s) for s in speakers])
        
        # Update messages with escalation flags
        for i, message in enumerate(processed_messages):
            message.escalation_flag = escalation_flags[i]
        
        # Detect overall escalation
        escalation_detected, escalation_reasons = detect_overall_escalation(sentiment_scores, texts, [str(s) for s in speakers])
        
        # Calculate overall sentiment
        overall_sentiment = calculate_overall_sentiment(sentiment_scores)
        
        # Determine final outcome (simple logic - can be enhanced)
        if escalation_detected:
            final_outcome = "escalated"
            # Trigger notification (email/webhook)
            try:
                from app.services.notification_service import NotificationService
                # Example: send email notification (replace with real config)
                NotificationService.send_email_notification(
                    to_email="admin@example.com",
                    subject=f"Escalation detected in conversation {conversation_in.thread_id}",
                    body=f"Conversation {conversation_in.thread_id} was escalated. Reasons: {escalation_reasons}",
                    smtp_server="smtp.example.com",
                    smtp_port=465,
                    smtp_user="your_smtp_user",
                    smtp_password="your_smtp_password"
                )
                # Example: send webhook notification (replace with real URL)
                NotificationService.send_webhook_notification(
                    webhook_url="https://your-webhook-url.com/notify",
                    payload={
                        "thread_id": conversation_in.thread_id,
                        "escalation_reasons": escalation_reasons
                    }
                )
            except Exception as notify_err:
                logger.error(f"Notification error: {notify_err}")
        else:
            final_outcome = "resolved"  # Placeholder - in real system, would check if resolved
        
        # Create conversation document
        conversation = Conversation(
            thread_id=conversation_in.thread_id,
            platform=conversation_in.platform or "unknown",
            messages=processed_messages,
            overall_sentiment_trend=sentiment_scores,
            overall_sentiment_label=processed_messages[0].sentiment_label if processed_messages else "Neutral",
            escalation_detected=escalation_detected,
            escalation_reasons=escalation_reasons,
            final_outcome=final_outcome
        )
        
        # Store in MongoDB (synchronous)
        try:
            # Check if conversation already exists
            existing = db["conversations"].find_one({"thread_id": conversation_in.thread_id})
            
            if existing:
                # Update existing conversation
                db["conversations"].update_one(
                    {"thread_id": conversation_in.thread_id},
                    {
                        "$set": {
                            "messages": [msg.dict() for msg in conversation.messages],
                            "overall_sentiment_trend": conversation.overall_sentiment_trend,
                            "escalation_detected": conversation.escalation_detected,
                            "escalation_reasons": conversation.escalation_reasons,
                            "final_outcome": conversation.final_outcome,
                            "updated_at": datetime.utcnow()
                        }
                    }
                )
                logger.info(f"Updated conversation {conversation_in.thread_id}")
            else:
                # Insert new conversation
                conv_dict = conversation.dict(by_alias=True, exclude_none=True)
                # Remove _id if it's None to let MongoDB auto-generate it
                conv_dict.pop("_id", None)
                result = db["conversations"].insert_one(conv_dict)
                logger.info(f"Stored conversation {conversation_in.thread_id} with ID {result.inserted_id}")
        
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
            raise
        
        # Prepare response
        sentiment_results = [
            SentimentAnalysisResult(
                message_id=msg.message_id,
                sentiment_score=msg.sentiment_score,
                sentiment_label=msg.sentiment_label,
                confidence=0.85  # Placeholder
            )
            for msg in processed_messages
        ]
        
        response = ConversationAnalysisResponse(
            thread_id=conversation_in.thread_id,
            message_count=len(processed_messages),
            sentiment_trajectory=sentiment_scores,
            overall_sentiment=overall_sentiment,
            escalation_detected=escalation_detected,
            escalation_reasons=escalation_reasons,
            messages_with_sentiment=sentiment_results
        )
        
        return response
    
    @staticmethod
    def get_conversation(thread_id: str) -> Optional[Conversation]:
        """Get conversation by thread_id"""
        db = get_database()
        conv = db["conversations"].find_one({"thread_id": thread_id})
        if conv:
            return Conversation(**conv)
        return None
    
    @staticmethod
    def get_all_conversations(limit: int = 100) -> List[Conversation]:
        """Get all conversations with limit"""
        db = get_database()
        conversations = list(db["conversations"].find().sort("created_at", DESCENDING).limit(limit))
        result = []
        for conv in conversations:
            try:
                result.append(Conversation(**conv))
            except Exception as e:
                logger.warning(f"Error deserializing conversation: {e}, data: {conv}")
                # Skip this conversation if it can't be deserialized
                continue
        return result
    
    @staticmethod
    def get_sentiment_trajectory(thread_id: str) -> Optional[List[dict]]:
        """Get sentiment trajectory for a conversation"""
        conversation = ConversationService.get_conversation(thread_id)
        if not conversation:
            return None
        
        trajectory = []
        for i, (score, message) in enumerate(zip(conversation.overall_sentiment_trend, conversation.messages)):
            trajectory.append({
                "turn": i + 1,
                "sentiment": score,
                "speaker": message.speaker,
                "escalation_point": message.escalation_flag
            })
        return trajectory

    @staticmethod
    def search_conversations(sentiment=None, escalated=None, platform=None, keyword=None, limit=100) -> List[Conversation]:
        """Search conversations by sentiment, escalation, platform, keyword"""
        db = get_database()
        query = {}
        if sentiment:
            query["overall_sentiment_label"] = sentiment
        if escalated is not None:
            query["escalation_detected"] = bool(escalated)
        if platform:
            query["platform"] = platform
        if keyword:
            query["messages.text"] = {"$regex": keyword, "$options": "i"}
        conversations = list(db["conversations"].find(query).sort("created_at", DESCENDING).limit(limit))
        result = []
        for conv in conversations:
            try:
                result.append(Conversation(**conv))
            except Exception as e:
                logger.warning(f"Error deserializing conversation: {e}, data: {conv}")
                continue
        return result
