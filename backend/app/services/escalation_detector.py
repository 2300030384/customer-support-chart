"""
Escalation Detection Service
Detects escalation based on multiple signals:
1. Two consecutive negative turns
2. Sharp sentiment drop (> 0.6 decrease)
3. Trigger words like "refund", "cancel", "angry", etc.
"""
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

# Escalation trigger words
TRIGGER_WORDS = {
    "refund", "cancel", "angry", "complaint", "not happy", "terrible",
    "hate", "horrible", "worst", "useless", "broken", "fraud", "scam",
    "lawsuit", "lawyer", "ceo", "manager", "escalate", "bug", "bug report"
}


def contains_trigger_words(text: str) -> Tuple[bool, List[str]]:
    """
    Check if text contains escalation trigger words
    
    Args:
        text: Message text to analyze
        
    Returns:
        Tuple: (has_trigger_words, list_of_found_words)
    """
    text_lower = text.lower()
    found_words = []
    
    for word in TRIGGER_WORDS:
        if word in text_lower:
            found_words.append(word)
    
    return len(found_words) > 0, found_words


def detect_consecutive_negatives(sentiment_scores: List[float], window_size: int = 2) -> Tuple[bool, List[int]]:
    """
    Detect consecutive negative sentiment turns
    
    Args:
        sentiment_scores: List of sentiment scores
        window_size: Number of consecutive turns to check (default 2)
        
    Returns:
        Tuple: (has_consecutive_negatives, list_of_escalation_message_indices)
    """
    escalation_indices = []
    
    for i in range(len(sentiment_scores) - window_size + 1):
        window = sentiment_scores[i:i + window_size]
        if all(score < -0.1 for score in window):
            escalation_indices.extend([i, i + 1])
    
    return len(escalation_indices) > 0, list(set(escalation_indices))


def detect_sentiment_drop(sentiment_scores: List[float], threshold: float = 0.6) -> Tuple[bool, List[int]]:
    """
    Detect sharp sentiment drops between consecutive messages
    
    Args:
        sentiment_scores: List of sentiment scores
        threshold: Minimum drop to flag as escalation (default 0.6)
        
    Returns:
        Tuple: (has_sentiment_drop, list_of_message_indices_with_drops)
    """
    escalation_indices = []
    
    for i in range(len(sentiment_scores) - 1):
        drop = sentiment_scores[i] - sentiment_scores[i + 1]
        if drop > threshold:
            escalation_indices.append(i + 1)
    
    return len(escalation_indices) > 0, escalation_indices


def detect_escalation_per_message(
    sentiment_scores: List[float],
    texts: List[str],
    speakers: List[str]
) -> Tuple[List[bool], str]:
    """
    Detect escalation flags for each message
    
    Args:
        sentiment_scores: List of sentiment scores
        texts: List of message texts
        speakers: List of speakers ("customer" or "agent")
        
    Returns:
        Tuple: (escalation_flags_per_message, escalation_reason)
    """
    escalation_flags = [False] * len(sentiment_scores)
    reason = ""
    
    # Check trigger words (customer messages only)
    for i, text in enumerate(texts):
        if speakers[i] == "customer":
            has_triggers, found = contains_trigger_words(text)
            if has_triggers:
                escalation_flags[i] = True
                reason = f"Trigger words found: {', '.join(found)}"
    
    # Check consecutive negatives
    has_consecutive, indices = detect_consecutive_negatives(sentiment_scores)
    if has_consecutive:
        for idx in indices:
            if idx < len(escalation_flags):
                escalation_flags[idx] = True
        reason = "Consecutive negative turns detected"
    
    # Check sentiment drop
    has_drop, indices = detect_sentiment_drop(sentiment_scores)
    if has_drop:
        for idx in indices:
            if idx < len(escalation_flags):
                escalation_flags[idx] = True
        reason = "Sharp sentiment drop detected"
    
    return escalation_flags, reason


def detect_overall_escalation(
    sentiment_scores: List[float],
    texts: List[str],
    speakers: List[str]
) -> Tuple[bool, List[str]]:
    """
    Detect overall conversation escalation with explanations
    
    Args:
        sentiment_scores: List of sentiment scores
        texts: List of message texts
        speakers: List of speakers
        
    Returns:
        Tuple: (escalation_detected, list_of_reasons)
    """
    reasons = []
    
    # Rule 1: Consecutive negatives
    has_consecutive, _ = detect_consecutive_negatives(sentiment_scores)
    if has_consecutive:
        reasons.append("Two or more consecutive negative turns detected")
    
    # Rule 2: Sharp sentiment drop
    has_drop, _ = detect_sentiment_drop(sentiment_scores)
    if has_drop:
        reasons.append("Sharp sentiment drop detected (> 0.6)")
    
    # Rule 3: Trigger words in customer messages
    for i, text in enumerate(texts):
        if speakers[i] == "customer":
            has_triggers, found = contains_trigger_words(text)
            if has_triggers:
                reasons.append(f"Escalation keywords found: {', '.join(found[:3])}")
                break
    
    # Rule 4: Overall negative trend
    if len(sentiment_scores) >= 3:
        recent_sentiment = sum(sentiment_scores[-3:]) / 3
        if recent_sentiment < -0.3:
            reasons.append("Recent sentiment trend is negative")
    
    escalation_detected = len(reasons) > 0
    
    return escalation_detected, reasons


def calculate_escalation_risk_score(
    sentiment_scores: List[float],
    escalation_flags: List[bool],
    has_trigger_words: bool
) -> float:
    """
    Calculate risk score (0 to 1) for escalation probability
    
    Args:
        sentiment_scores: List of sentiment scores
        escalation_flags: Escalation flags per message
        has_trigger_words: Whether trigger words are present
        
    Returns:
        Risk score from 0 to 1
    """
    score = 0.0
    
    # Negative sentiment score: up to 0.3 points
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    if avg_sentiment < -0.5:
        score += 0.3
    elif avg_sentiment < -0.2:
        score += 0.15
    
    # Escalation flags: up to 0.4 points
    escalation_rate = sum(escalation_flags) / len(escalation_flags) if escalation_flags else 0
    score += escalation_rate * 0.4
    
    # Trigger words: up to 0.3 points
    if has_trigger_words:
        score += 0.3
    
    return min(score, 1.0)
