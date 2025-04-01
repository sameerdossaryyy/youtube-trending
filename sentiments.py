from textblob import TextBlob
import re
from functools import lru_cache

def clean_text(text):
    """Remove URLs, mentions, and hashtags"""
    text = re.sub(r'http\S+|@\w+|#\w+', '', text)
    return text.strip()

@lru_cache(maxsize=1000)
def analyze_sentiment(text):
    """Enhanced sentiment analysis with emoji labels"""
    cleaned = clean_text(text)
    analysis = TextBlob(cleaned)
    polarity = analysis.sentiment.polarity
    
    # Emotion classification
    if polarity > 0.5:
        emotion = "😊 Strongly Positive"
    elif polarity > 0.1:
        emotion = "🙂 Positive"
    elif polarity < -0.5:
        emotion = "😡 Strongly Negative"
    elif polarity < -0.1:
        emotion = "☹️ Negative"
    else:
        emotion = "😐 Neutral"
    
    return {
        "polarity": round(polarity, 2),
        "subjectivity": round(analysis.sentiment.subjectivity, 2),
        "emotion": emotion
    }
