"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database.connection import connect_to_mongo, close_mongo_connection
from app.routes import health, conversations, analytics, predictions, auth, search, chatbot, escalation_rules, export
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting Sentiment Analysis API...")
    await connect_to_mongo()
    logger.info("✓ Application started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    await close_mongo_connection()
    logger.info("✓ Application shut down gracefully")


# Create FastAPI app
app = FastAPI(
    title="Sentiment Analysis in Customer Support",
    description="AI-powered sentiment analysis and escalation detection for support conversations",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"✓ CORS enabled for origins: {settings.cors_origins}")


# Include routers
app.include_router(health.router)
app.include_router(conversations.router)
app.include_router(analytics.router)
app.include_router(predictions.router)
app.include_router(auth.router)
app.include_router(search.router)
app.include_router(chatbot.router)
app.include_router(escalation_rules.router)
app.include_router(export.router)
from app.routes import webhook, model
app.include_router(webhook.router)
app.include_router(model.router)

logger.info("✓ All route handlers registered")


# Custom exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "detail": "Internal server error",
        "error": str(exc) if settings.debug else "An error occurred"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
