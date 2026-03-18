"""ML Prediction routes"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.services.early_warning import predict_early_warning
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["ML Predictions"], prefix="/predict")


class EarlyWarningInput(BaseModel):
    """Input for early warning prediction"""
    thread_id: str = Field(..., description="Unique conversation thread ID")
    customer_messages: List[str] = Field(..., description="List of customer messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "thread_id": "chat_12345",
                "customer_messages": [
                    "Hey, I have an issue with my order",
                    "It's been 2 days and nothing has changed",
                    "This is terrible, I want a refund"
                ]
            }
        }


@router.post("/early-warning")
async def predict_early_warning_endpoint(input_data: EarlyWarningInput):
    """
    Predict escalation risk using first 3 customer turns
    
    Uses ML classifier (TF-IDF + Logistic Regression) trained on historical data.
    
    Returns:
        - escalation_probability: Probability of escalation (0-1)
        - risk_level: "low", "medium", or "high"
        - warning_reasons: List of reasons for the prediction
    """
    try:
        prediction = predict_early_warning(
            input_data.customer_messages,
            input_data.thread_id
        )
        return prediction.dict()
    except Exception as e:
        logger.error(f"Error in early warning prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
