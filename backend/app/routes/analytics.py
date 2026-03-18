"""Analytics routes"""
from fastapi import APIRouter, HTTPException, Query
from app.services.analytics_service import AnalyticsService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Analytics"], prefix="/analytics")


@router.get("/overview")
async def get_overview():
    """
    Get analytics overview
    
    Returns:
        - total_threads: Total conversations analyzed
        - escalated_threads: Number of escalated conversations
        - escalation_rate: Percentage of escalated conversations
        - avg_sentiment: Average sentiment across all conversations
    """
    try:
        overview = AnalyticsService.get_overview()
        return overview.dict()
    except Exception as e:
        logger.error(f"Error getting analytics overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/funnel")
async def get_funnel():
    """
    Get funnel analytics (conversation outcomes)
    
    Returns:
        - resolved: Conversations marked as resolved
        - escalated: Conversations that escalated
        - unresolved: Conversations still unresolved
    """
    try:
        funnel = AnalyticsService.get_funnel()
        return funnel.dict()
    except Exception as e:
        logger.error(f"Error getting funnel data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sentiment-distribution")
async def get_sentiment_distribution():
    """Get distribution of sentiment labels across all conversations"""
    try:
        distribution = AnalyticsService.get_sentiment_distribution()
        return {
            "distribution": distribution,
            "total": sum(distribution.values())
        }
    except Exception as e:
        logger.error(f"Error getting sentiment distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sentiment-over-time")
async def get_sentiment_over_time(days: int = Query(30, ge=1, le=365)):
    """
    Get average sentiment over time periods
    
    Args:
        days: Number of days to look back (default 30)
    """
    try:
        data = AnalyticsService.get_sentiment_over_time(days=days)
        return {
            "days": days,
            "data": data
        }
    except Exception as e:
        logger.error(f"Error getting sentiment over time: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/escalation-playbook")
async def get_escalation_playbook():
    """
    Get insights and recommendations from escalated conversations
    
    Returns:
        - top_negative_keywords: Most common negative words
        - failure_patterns: Common issues leading to escalation
        - avg_time_before_escalation: Average minutes before escalation
        - recommended_actions: Actionable recommendations
    """
    try:
        playbook = AnalyticsService.get_escalation_playbook()
        return playbook.dict()
    except Exception as e:
        logger.error(f"Error getting escalation playbook: {e}")
        raise HTTPException(status_code=500, detail=str(e))
