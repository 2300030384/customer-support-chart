"""
Analytics Service
Provides analytics data for overview and funnel charts
"""
from typing import List
from datetime import datetime, timedelta
from pymongo import DESCENDING
from app.database.connection import get_database
from app.models.schemas import AnalyticsOverview, FunnelData, NegativeKeyword, FailurePattern, EscalationPlaybook
from app.services.escalation_detector import TRIGGER_WORDS
from collections import Counter
import logging
import re

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics and reporting"""
    
    @staticmethod
    def get_overview() -> AnalyticsOverview:
        """Get overall analytics overview"""
        db = get_database()
        conversations = list(db["conversations"].find({}))
        
        total_threads = len(conversations)
        escalated_count = sum(1 for c in conversations if c.get("escalation_detected", False))
        resolved_count = sum(1 for c in conversations if c.get("final_outcome") == "resolved")
        unresolved_count = sum(1 for c in conversations if c.get("final_outcome") == "unresolved")
        
        escalation_rate = (escalated_count / total_threads * 100) if total_threads > 0 else 0
        
        # Calculate average sentiment
        all_sentiments = []
        for conv in conversations:
            trend = conv.get("overall_sentiment_trend", [])
            if trend:
                all_sentiments.extend(trend)
        
        avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0
        
        return AnalyticsOverview(
            total_threads=total_threads,
            escalated_threads=escalated_count,
            unresolved_threads=unresolved_count,
            resolved_threads=resolved_count,
            escalation_rate=round(escalation_rate, 2),
            avg_sentiment=round(avg_sentiment, 3)
        )
        
        total_threads = len(conversations)
        escalated_count = sum(1 for c in conversations if c.get("escalation_detected", False))
        resolved_count = sum(1 for c in conversations if c.get("final_outcome") == "resolved")
        unresolved_count = sum(1 for c in conversations if c.get("final_outcome") == "unresolved")
        
        escalation_rate = (escalated_count / total_threads * 100) if total_threads > 0 else 0
        
        # Calculate average sentiment
        all_sentiments = []
        for conv in conversations:
            trend = conv.get("overall_sentiment_trend", [])
            if trend:
                all_sentiments.extend(trend)
        
        avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0
        
        return AnalyticsOverview(
            total_threads=total_threads,
            escalated_threads=escalated_count,
            unresolved_threads=unresolved_count,
            resolved_threads=resolved_count,
            escalation_rate=round(escalation_rate, 2),
            avg_sentiment=round(avg_sentiment, 3)
        )
    
    @staticmethod
    def get_funnel() -> FunnelData:
        """Get funnel data"""
        db = get_database()
        conversations = list(db["conversations"].find({}))
        
        resolved = sum(1 for c in conversations if c.get("final_outcome") == "resolved")
        escalated = sum(1 for c in conversations if c.get("final_outcome") == "escalated")
        unresolved = sum(1 for c in conversations if c.get("final_outcome") == "unresolved")
        
        return FunnelData(resolved=resolved, escalated=escalated, unresolved=unresolved)
    
    @staticmethod
    def get_sentiment_distribution() -> dict:
        """Get sentiment distribution across all conversations"""
        db = get_database()
        conversations = list(db["conversations"].find({}))
        
        distribution = {"Positive": 0, "Neutral": 0, "Negative": 0}
        
        for conv in conversations:
            messages = conv.get("messages", [])
            for msg in messages:
                label = msg.get("sentiment_label", "Neutral")
                if label in distribution:
                    distribution[label] += 1
        
        return distribution
    
    @staticmethod
    def get_escalation_playbook() -> EscalationPlaybook:
        """Analyze escalated conversations and extract insights"""
        db = get_database()
        escalated_conversations = list(db["conversations"].find(
            {"escalation_detected": True}
        ))
        
        total_escalated = len(escalated_conversations)
        logger.info(f"Analyzing {total_escalated} escalated conversations")
        
        # Extract top negative keywords
        keyword_counter: Counter = Counter()
        response_delays = []
        time_to_escalations = []
        failure_patterns_list = []
        
        for conv in escalated_conversations:
            messages = conv.get("messages", [])
            created_at = conv.get("created_at", datetime.utcnow())
            
            # Extract keywords from customer messages
            for msg in messages:
                if msg.get("speaker") == "customer":
                    text = msg.get("text", "").lower()
                    for word in TRIGGER_WORDS:
                        if word in text:
                            keyword_counter[word] += 1
                    
                    # Extract other negative words
                    words = re.findall(r'\b\w+\b', text)
                    for w in words:
                        if len(w) > 3:  # Skip short words
                            keyword_counter[w] += 1
            
            # Calculate response delays (difference between consecutive messages)
            if len(messages) > 1:
                for i in range(1, len(messages)):
                    prev_time = messages[i-1].get("timestamp")
                    curr_time = messages[i].get("timestamp")
                    if prev_time and curr_time:
                        delay = (curr_time - prev_time).total_seconds() / 60
                        response_delays.append(delay)
            
            # Calculate time to escalation
            escalation_msg_idx = next((i for i, m in enumerate(messages) if m.get("escalation_flag")), None)
            if escalation_msg_idx:
                time_to_escalations.append(escalation_msg_idx * 5)  # Approximate minutes
            
            # Identify failure patterns
            sentiment_trend = conv.get("overall_sentiment_trend", [])
            if len(sentiment_trend) >= 2:
                drop = sentiment_trend[0] - sentiment_trend[-1]
                if drop > 0.5:
                    failure_patterns_list.append("Negative sentiment progression")
        
        # Prepare top keywords
        max_count = max(keyword_counter.values()) if keyword_counter.values() else 1
        top_keywords = [
            NegativeKeyword(
                keyword=word,
                frequency=count,
                sentiment_impact=-0.3 * (count / max_count)
            )
            for word, count in keyword_counter.most_common(10)
        ]
        
        # Prepare failure patterns
        pattern_counter = Counter(failure_patterns_list)
        failure_patterns = [
            FailurePattern(
                pattern=pattern,
                occurrences=count,
                avg_time_to_escalation_minutes=sum(time_to_escalations) / len(time_to_escalations) if time_to_escalations else 0
            )
            for pattern, count in pattern_counter.most_common(5)
        ]
        
        # Calculate averages
        avg_time_before_escalation = sum(time_to_escalations) / len(time_to_escalations) if time_to_escalations else 0
        avg_response_delay = sum(response_delays) / len(response_delays) if response_delays else 0
        
        # Recommend actions
        recommendations = []
        if avg_response_delay > 10:
            recommendations.append("Improve agent response time (currently > 10 minutes)")
        if top_keywords:
            recommendations.append(f"Train agents to handle conversations with '{top_keywords[0].keyword}'")
        if avg_time_before_escalation < 15:
            recommendations.append("Implement early intervention system to prevent quick escalations")
        
        if not recommendations:
            recommendations.append("Continue monitoring for escalation patterns")
        
        return EscalationPlaybook(
            total_escalated_conversations=total_escalated,
            top_negative_keywords=top_keywords,
            most_common_failure_patterns=failure_patterns,
            avg_time_before_escalation_minutes=round(avg_time_before_escalation, 2),
            common_agent_response_delay_minutes=round(avg_response_delay, 2),
            recommended_actions=recommendations
        )
    
    @staticmethod
    def get_sentiment_over_time(days: int = 30) -> List[dict]:
        """Get average sentiment over time periods"""
        db = get_database()
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        conversations = list(db["conversations"].find(
            {"created_at": {"$gte": cutoff_date}}
        ))
        
        # Group by date
        daily_sentiments: dict = {}
        for conv in conversations:
            created_at = conv.get("created_at", datetime.utcnow())
            date_key = created_at.strftime("%Y-%m-%d")
            
            trend = conv.get("overall_sentiment_trend", [])
            if trend:
                avg = sum(trend) / len(trend)
                if date_key not in daily_sentiments:
                    daily_sentiments[date_key] = []
                daily_sentiments[date_key].append(avg)
        
        # Calculate daily averages
        result = []
        for date_key in sorted(daily_sentiments.keys()):
            sentiments = daily_sentiments[date_key]
            avg_sentiment = sum(sentiments) / len(sentiments)
            result.append({
                "date": date_key,
                "avg_sentiment": round(avg_sentiment, 3),
                "conversation_count": len(sentiments)
            })
        
        return result
