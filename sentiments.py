from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return {
        "polarity": analysis.sentiment.polarity,  # -1 to 1 (negative to positive)
        "subjectivity": analysis.sentiment.subjectivity  # 0 to 1 (fact to opinion)
    }

# Apply to video titles
for video in videos:
    sentiment = analyze_sentiment(video["title"])
    video.update(sentiment)
