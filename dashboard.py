import streamlit as st
from datetime import datetime
from trending import get_trending_videos
from sentiments import analyze_sentiment
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def format_duration(seconds):
    """Convert seconds to HH:MM:SS"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def display_videos(videos):
    """Display videos with genre and sentiment filters"""
    st.title("🎬 YouTube Trending Dashboard")
    
    # ---- Filters ----
    col1, col2 = st.columns(2)
    
    with col1:
        # Genre filter (dynamic based on available categories)
        available_categories = sorted(list({v['category'] for v in videos if v['category']}))
        selected_categories = st.multiselect(
            "📺 Filter by Category",
            options=available_categories,
            default=["Music", "Gaming"]
        )
    
    with col2:
        # Sentiment filter
        sentiment_filter = st.radio(
            "🎭 Filter by Sentiment",
            options=["All", "Positive 😊", "Neutral 😐", "Negative 😠"],
            horizontal=True
        )
    
    # ---- Filter Logic ----
    filtered_videos = []
    for video in videos:
        # Category filter
        category_match = (
            not selected_categories or
            video.get('category') in selected_categories
        )
        
        # Sentiment filter
        sentiment = analyze_sentiment(video['title'])
        sentiment_match = (
            sentiment_filter == "All" or
            (sentiment_filter == "Positive 😊" and "Positive" in sentiment['emotion']) or
            (sentiment_filter == "Negative 😠" and "Negative" in sentiment['emotion']) or
            (sentiment_filter == "Neutral 😐" and sentiment['emotion'] == "😐 Neutral")
        )
        
        if category_match and sentiment_match:
            filtered_videos.append(video)
    
    # ---- Display Results ----
    st.subheader(f"📊 Results: {len(filtered_videos)} videos")
    
    for video in filtered_videos:
        with st.expander(f"{video['title']}", expanded=False):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.image(video['thumbnail'], use_column_width=True)
                
            with col2:
                # Sentiment analysis
                sentiment = analyze_sentiment(video['title'])
                st.markdown(
                    f"**Sentiment:** "
                    f"<span style='color: {'green' if 'Positive' in sentiment['emotion'] else 'red' if 'Negative' in sentiment['emotion'] else 'gray'}'>{sentiment['emotion']}</span> "
                    f"(Polarity: {sentiment['polarity']})",
                    unsafe_allow_html=True
                )
                
                # Video metadata
                st.write(f"**Channel:** {video['channelTitle']}")
                st.write(f"**Category:** {video.get('category', 'Unknown')}")
                st.write(f"**Views:** {video['viewCount']}")
                st.write(f"**Published:** {datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')}")
                st.link_button("▶️ Watch on YouTube", f"https://youtu.be/{video['videoId']}")

def main():
    try:
        # Get trending videos
        videos = get_trending_videos(API_KEY, region_code="IN", max_results=50)
        
        if not videos:
            st.error("No videos found. Check your API key or network connection.")
            return
        
        # Display dashboard
        display_videos(videos)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
