from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    # Enhanced emotion classification
    if polarity > 0.3:
        emotion = "😊 Positive"
    elif polarity < -0.3:
        emotion = "😠 Negative"
    else:
        emotion = "😐 Neutral"
    
    return {
        "polarity": round(polarity, 2),
        "subjectivity": round(analysis.sentiment.subjectivity, 2),
        "emotion": emotion
    }
