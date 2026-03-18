from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
OPENAI_API_KEY = os.getenv("Sankar")

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # MongoDB Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "sentiment_db"
    
    # Application Configuration
    environment: str = "development"
    debug: bool = True
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
    
    # Sentiment Analysis Configuration
    sentiment_model: str = "vader"  # Options: "vader", "huggingface"
    openai_api_key: str
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "validate_by_name": True
    }


settings = Settings()
print('DEBUG openai_api_key:', settings.openai_api_key)
