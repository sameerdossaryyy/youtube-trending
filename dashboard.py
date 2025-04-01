import streamlit as st
import pandas as pd
import plotly.express as px
from googleapiclient.discovery import build
from textblob import TextBlob

#define all functions
def get_trending_videos(api_key, region_code="US", max_results=10):
    youtube = build("youtube", "v3", developerKey=api_key)
    
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()
    
    videos = []
    for item in response["items"]:
        videos.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0)),
            "published_at": item["snippet"]["publishedAt"]
        })
    return videos

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return {
        "polarity": analysis.sentiment.polarity,
        "subjectivity": analysis.sentiment.subjectivity
    }

#fetch data
API_KEY = "AIzaSyBPNU6Dr2AKfrYhz7KA-ekCBoANtpOrOxI"  
videos = get_trending_videos(API_KEY)

#sentiment analysis
for video in videos:
    video.update(analyze_sentiment(video["title"]))

#dashboard
st.title("📈 YouTube Trending Analyzer")
df = pd.DataFrame(videos)

# Metrics
st.metric("Total Videos Analyzed", len(df))
st.metric("Average Likes", f"{df['likes'].mean():,.0f}")

# Data table
st.dataframe(df[['title', 'channel', 'views', 'likes']].sort_values("views", ascending=False))

# Visualizations
fig = px.bar(df, x="title", y="views", title="View Counts")
st.plotly_chart(fig)

fig2 = px.scatter(df, x="polarity", y="likes", color="comments", 
                 title="Sentiment vs Engagement")
st.plotly_chart(fig2)
