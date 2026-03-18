from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal, Annotated
from datetime import datetime
from bson import ObjectId


# Pydantic 2.x style validator for ObjectId
def validate_object_id(v):
    """Validate ObjectId - accept ObjectId, string, or None"""
    if v is None:
        return None
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str):
        if ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError(f"Invalid ObjectId string: {v}")
    raise ValueError(f"Invalid ObjectId type: {type(v)}")


# ============ Message Schemas ============
class MessageIn(BaseModel):
    """Input message model"""
    speaker: Literal["customer", "agent"]
    text: str
    timestamp: datetime


class Message(MessageIn):
    """Message model with sentiment analysis"""
    message_id: str = Field(default_factory=lambda: str(ObjectId()))
    sentiment_score: float = Field(ge=-1, le=1, description="Sentiment score from -1 to +1")
    sentiment_label: Literal["Negative", "Neutral", "Positive"]
    escalation_flag: bool = False


# ============ Conversation Schemas ============
class ConversationIn(BaseModel):
    """Input conversation model for creating/uploading"""
    thread_id: str
    platform: Optional[str] = "unknown"
    messages: List[MessageIn]


class Conversation(BaseModel):
    """Complete conversation model with analysis"""
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    thread_id: str
    platform: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[Message]
    overall_sentiment_trend: List[float] = Field(description="Sentiment scores over time")
    overall_sentiment_label: Optional[Literal["Negative", "Neutral", "Positive"]] = None
    escalation_detected: bool = False
    escalation_reasons: List[str] = []
    final_outcome: Literal["resolved", "escalated", "unresolved"] = "unresolved"
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        return validate_object_id(v)
    
    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ============ Response Schemas ============
class SentimentAnalysisResult(BaseModel):
    """Sentiment analysis result for a single turn"""
    message_id: str
    sentiment_score: float
    sentiment_label: Literal["Negative", "Neutral", "Positive"]
    confidence: float = Field(ge=0, le=1)


class ConversationAnalysisResponse(BaseModel):
    """Response after analyzing and storing a conversation"""
    thread_id: str
    message_count: int
    sentiment_trajectory: List[float]
    overall_sentiment: float
    escalation_detected: bool
    escalation_reasons: List[str]
    messages_with_sentiment: List[SentimentAnalysisResult]


class AnalyticsOverview(BaseModel):
    """Overview analytics"""
    total_threads: int
    escalated_threads: int
    unresolved_threads: int
    resolved_threads: int
    escalation_rate: float = Field(ge=0, le=100)
    avg_sentiment: float


class FunnelData(BaseModel):
    """Funnel analytics"""
    resolved: int
    escalated: int
    unresolved: int


class SentimentTrajectory(BaseModel):
    """Sentiment trajectory for a conversation"""
    turn: int
    sentiment: float
    speaker: str
    escalation_point: bool = False


class AnalyticsFunnel(BaseModel):
    """Funnel chart data"""
    category: str
    value: int


class EarlyWarningPrediction(BaseModel):
    """Early warning prediction result"""
    thread_id: str
    escalation_probability: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    risk_level: Literal["low", "medium", "high"]
    warning_reasons: List[str] = []


class NegativeKeyword(BaseModel):
    """Negative keyword with frequency"""
    keyword: str
    frequency: int
    sentiment_impact: float


class FailurePattern(BaseModel):
    """Common failure pattern"""
    pattern: str
    occurrences: int
    avg_time_to_escalation_minutes: float


class EscalationPlaybook(BaseModel):
    """Analytics playbook for escalation insights"""
    total_escalated_conversations: int
    top_negative_keywords: List[NegativeKeyword]
    most_common_failure_patterns: List[FailurePattern]
    avg_time_before_escalation_minutes: float
    common_agent_response_delay_minutes: float
    recommended_actions: List[str]
