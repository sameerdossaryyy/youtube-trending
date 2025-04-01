import os
from datetime import timedelta
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def parse_youtube_duration(duration):
    """
    Convert YouTube duration (ISO 8601) to seconds.
    Examples:
    - "PT24M" → 1440 (24 minutes)
    - "PT2H30M" → 9000 (2.5 hours)
    - "PT1M30S" → 90 (1.5 minutes)
    """
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0
    
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0
    
    return timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    ).total_seconds()

def get_trending_videos(api_key, region_code="US", max_results=50):
    """
    Fetch trending videos from YouTube API
    Returns list of videos with parsed durations
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response.get('items', []):
            video = {
                'title': item['snippet']['title'],
                'channelTitle': item['snippet']['channelTitle'],
                'viewCount': item['statistics'].get('viewCount', '0'),
                'duration': parse_youtube_duration(item['contentDetails']['duration']),
                'publishedAt': item['snippet']['publishedAt'],
                'videoId': item['id']
            }
            videos.append(video)
        
        return videos
    
    except Exception as e:
        print(f"Error fetching trending videos: {e}")
        return []
