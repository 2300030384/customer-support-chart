"""
Early Warning ML Classifier
Uses first 3 customer turns to predict escalation probability
Uses TF-IDF + Logistic Regression (scikit-learn)
"""
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle
import os
import logging
from datetime import datetime
from app.models.schemas import EarlyWarningPrediction

logger = logging.getLogger(__name__)

MODEL_PATH = "ml_models/escalation_classifier.pkl"


class EarlyWarningClassifier:
    """ML classifier for early escalation prediction"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_or_create_model()
    
    def load_or_create_model(self):
        """Load existing model or create new one"""
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"✓ Loaded existing ML model from {MODEL_PATH}")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Creating new one.")
                self._create_new_model()
        else:
            self._create_new_model()
    
    def _create_new_model(self):
        """Create a new model"""
        # TF-IDF + Logistic Regression pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=100, ngram_range=(1, 2))),
            ('clf', LogisticRegression(random_state=42, max_iter=200))
        ])
        logger.info("✓ Created new ML model pipeline")
    
    def train(self, texts: List[str], labels: List[int], save: bool = True):
        """
        Train the model on conversation data
        
        Args:
            texts: List of conversation texts (first 3 customer turns)
            labels: List of escalation labels (1 = escalated, 0 = not escalated)
            save: Whether to save model after training
        """
        try:
            if self.model is None:
                self._create_new_model()
            
            self.model.fit(texts, labels)
            logger.info(f"✓ Trained ML model on {len(texts)} samples")
            
            if save:
                self.save_model()
        
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise
    
    def predict(self, text: str) -> Tuple[int, float]:
        """
        Predict escalation for a text
        
        Args:
            text: Conversation text
            
        Returns:
            Tuple: (prediction, probability)
        """
        if self.model is None:
            logger.warning("Model not initialized, returning neutral prediction")
            return 0, 0.5
        
        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            probability = probabilities[1]  # Probability of escalation
            
            return prediction, probability
        
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return 0, 0.5
    
    def save_model(self):
        """Save model to disk"""
        try:
            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            with open(MODEL_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            logger.info(f"✓ Saved ML model to {MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")


# Global classifier instance
classifier = EarlyWarningClassifier()


def predict_early_warning(
    customer_messages: List[str],
    thread_id: str,
    use_first_n_turns: int = 3
) -> EarlyWarningPrediction:
    """
    Predict escalation risk using only first N customer turns
    
    Args:
        customer_messages: List of customer messages
        thread_id: Conversation thread ID
        use_first_n_turns: Use first N customer turns (default 3)
        
    Returns:
        EarlyWarningPrediction with probability and risk level
    """
    # Take first N messages
    selected_messages = customer_messages[:use_first_n_turns]
    combined_text = " ".join(selected_messages)
    
    if not combined_text.strip():
        return EarlyWarningPrediction(
            thread_id=thread_id,
            escalation_probability=0.0,
            confidence=0.0,
            risk_level="low",
            warning_reasons=["No conversation data to analyze"]
        )
    
    # Predict
    prediction, probability = classifier.predict(combined_text)
    
    # Determine risk level and reasons
    risk_level = "low"
    warning_reasons = []
    
    if probability > 0.7:
        risk_level = "high"
        warning_reasons.append("High escalation probability detected")
    elif probability > 0.4:
        risk_level = "medium"
        warning_reasons.append("Moderate escalation risk")
    
    # Check for trigger words (simple heuristic)
    from app.services.escalation_detector import TRIGGER_WORDS
    trigger_found = []
    for word in TRIGGER_WORDS:
        if word in combined_text.lower():
            trigger_found.append(word)
    
    if trigger_found:
        warning_reasons.append(f"Contains keywords: {', '.join(trigger_found[:2])}")
    
    # Check sentiment (if enough data available)
    from app.services.sentiment_analyzer import analyze_turn
    sentiment_scores = []
    for msg in selected_messages:
        score, _, _ = analyze_turn(msg)
        sentiment_scores.append(score)
    
    if sentiment_scores:
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        if avg_sentiment < -0.2:
            warning_reasons.append("Negative sentiment detected early")
    
    return EarlyWarningPrediction(
        thread_id=thread_id,
        escalation_probability=round(probability, 3),
        confidence=abs(probability - 0.5) * 2,  # Confidence increases as we move away from 0.5
        risk_level=risk_level,
        warning_reasons=warning_reasons
    )


def train_classifier_from_conversations(conversations: List[dict]):
    """
    Train classifier using existing conversations
    
    Args:
        conversations: List of conversation documents from MongoDB
    """
    texts = []
    labels = []
    
    for conv in conversations:
        messages = conv.get("messages", [])
        escalated = conv.get("escalation_detected", False)
        
        # Extract first 3 customer messages
        customer_messages = [
            m.get("text", "") for m in messages 
            if m.get("speaker") == "customer"
        ][:3]
        
        if customer_messages:
            combined = " ".join(customer_messages)
            texts.append(combined)
            labels.append(1 if escalated else 0)
    
    if texts:
        classifier.train(texts, labels)
        logger.info(f"✓ Trained early warning classifier on {len(texts)} conversations")
