"""
Sentiment Analysis Service
Supports both VADER (lightweight) and HuggingFace transformers
"""
from typing import Tuple, List, Literal
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging

logger = logging.getLogger(__name__)

# Initialize VADER analyzer (lightweight, no downloads needed)
vader_analyzer = SentimentIntensityAnalyzer()


def get_sentiment_label(score: float) -> Literal["Negative", "Neutral", "Positive"]:
    """
    Convert sentiment score to label
    
    Args:
        score: Float between -1 and 1
        
    Returns:
        Sentiment label: "Negative", "Neutral", or "Positive"
    """
    if score < -0.1:
        return "Negative"
    elif score > 0.1:
        return "Positive"
    else:
        return "Neutral"


def analyze_turn_vader(text: str) -> Tuple[float, Literal["Negative", "Neutral", "Positive"], float]:
    """
    Analyze sentiment of a single message using VADER
    
    Args:
        text: Message text to analyze
        
    Returns:
        Tuple: (sentiment_score, sentiment_label, confidence)
    """
    try:
        scores = vader_analyzer.polarity_scores(text)
        compound_score = scores["compound"]  # -1 to 1
        
        label = get_sentiment_label(compound_score)
        confidence = scores.get(label.lower(), 0)
        
        return compound_score, label, confidence
    except Exception as e:
        logger.error(f"Error analyzing sentiment with VADER: {e}")
        return 0.0, "Neutral", 0.0


def analyze_turn_huggingface(text: str) -> Tuple[float, Literal["Negative", "Neutral", "Positive"], float]:
    """
    Analyze sentiment using HuggingFace transformers
    Falls back to VADER if transformers not available
    
    Args:
        text: Message text to analyze
        
    Returns:
        Tuple: (sentiment_score, sentiment_label, confidence)
    """
    try:
        from transformers import pipeline
        
        # Use distilbert for faster inference
        classifier = pipeline("sentiment-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = classifier(text[:512])  # Limit to 512 tokens
        
        label = result[0]["label"].lower()
        score = result[0]["score"]
        confidence = score
        
        # Convert to -1 to 1 range
        if label == "negative":
            sentiment_score = -score
        else:
            sentiment_score = score
            
        return sentiment_score, get_sentiment_label(sentiment_score), confidence
        
    except Exception as e:
        logger.warning(f"HuggingFace model not available, falling back to VADER: {e}")
        return analyze_turn_vader(text)


def analyze_turn(text: str, use_vader: bool = True) -> Tuple[float, Literal["Negative", "Neutral", "Positive"], float]:
    """
    Analyze sentiment of a single message (turn)
    
    Args:
        text: Message text
        use_vader: If True, use VADER; if False, try HuggingFace
        
    Returns:
        Tuple: (sentiment_score, sentiment_label, confidence)
    """
    if use_vader:
        return analyze_turn_vader(text)
    else:
        return analyze_turn_huggingface(text)


def analyze_conversation(messages: List[str], use_vader: bool = True) -> List[float]:
    """
    Analyze sentiment trajectory across a conversation
    
    Args:
        messages: List of message texts
        use_vader: If True, use VADER; if False, try HuggingFace
        
    Returns:
        List of sentiment scores
    """
    trajectory = []
    for message in messages:
        score, _, _ = analyze_turn(message, use_vader=use_vader)
        trajectory.append(score)
    return trajectory


def calculate_overall_sentiment(sentiment_scores: List[float]) -> float:
    """
    Calculate overall sentiment from a list of scores
    
    Args:
        sentiment_scores: List of sentiment scores
        
    Returns:
        Overall average sentiment score
    """
    if not sentiment_scores:
        return 0.0
    return sum(sentiment_scores) / len(sentiment_scores)


def get_sentiment_distribution(sentiment_labels: List[str]) -> dict:
    """
    Get distribution of sentiment labels
    
    Args:
        sentiment_labels: List of sentiment labels
        
    Returns:
        Dictionary with counts
    """
    distribution = {
        "Positive": 0,
        "Neutral": 0,
        "Negative": 0
    }
    for label in sentiment_labels:
        if label in distribution:
            distribution[label] += 1
    return distribution
