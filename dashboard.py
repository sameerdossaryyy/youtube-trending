import streamlit as st
from datetime import datetime
from trending import get_trending_videos, parse_youtube_duration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def format_duration(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def display_videos(videos):
    """Display trending videos in Streamlit"""
    st.title("YouTube Trending Videos Dashboard")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        min_duration = st.slider("Minimum duration (minutes)", 0, 120, 0)
    with col2:
        max_duration = st.slider("Maximum duration (minutes)", 0, 120, 120)
    
    # Convert to seconds
    min_seconds = min_duration * 60
    max_seconds = max_duration * 60
    
    # Filter videos
    filtered_videos = [
        v for v in videos 
        if min_seconds <= v['duration'] <= max_seconds
    ]
    
    # Display metrics
    st.metric("Total Videos", len(filtered_videos))
    
    # Display table
    for idx, video in enumerate(filtered_videos, start=1):
        with st.expander(f"{idx}. {video['title']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.image(f"https://img.youtube.com/vi/{video['videoId']}/mqdefault.jpg")
            with col2:
                st.write(f"**Channel:** {video['channelTitle']}")
                st.write(f"**Views:** {video['viewCount']}")
                st.write(f"**Duration:** {format_duration(video['duration'])}")
                st.write(f"**Published:** {datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')}")
                st.link_button("Watch on YouTube", f"https://youtu.be/{video['videoId']}")

def main():
    try:
        # Get trending videos
        videos = get_trending_videos(API_KEY, region_code="US", max_results=50)
        
        if not videos:
            st.error("No videos found. Check your API key or network connection.")
            return
        
        # Display the dashboard
        display_videos(videos)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
