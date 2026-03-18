"""Health check and basic routes"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.database.connection import get_database

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Verifies database connection and returns system status
    """
    try:
        db = get_database()
        # Ping database (synchronous operation)
        db.client.admin.command('ping')
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sentiment Analysis API for Customer Support",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/upload-thread",
            "analytics": "/analytics/overview",
            "docs": "/docs"
        }
    }
