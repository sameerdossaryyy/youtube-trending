import os
from datetime import timedelta
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

def parse_youtube_duration(duration):
    """Convert ISO 8601 duration to seconds"""
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
    """Fetch trending videos with category data"""
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    try:
        # Get videos
        video_request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results
        )
        video_response = video_request.execute()
        
        # Get category names
        category_request = youtube.videoCategories().list(
            part="snippet",
            regionCode=region_code
        )
        category_response = category_request.execute()
        categories = {int(item['id']): item['snippet']['title'] 
                     for item in category_response.get('items', [])}
        
        # Process videos
        videos = []
        for item in video_response.get('items', []):
            video_data = {
                'title': item['snippet']['title'],
                'channelTitle': item['snippet']['channelTitle'],
                'viewCount': item['statistics'].get('viewCount', 'N/A'),
                'duration': parse_youtube_duration(item['contentDetails']['duration']),
                'categoryId': item['snippet'].get('categoryId'),
                'category': categories.get(int(item['snippet'].get('categoryId', 0))), 
                'publishedAt': item['snippet']['publishedAt'],
                'videoId': item['id'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            }
            videos.append(video_data)
        
        return videos
    
    except Exception as e:
        print(f"Error fetching trending videos: {e}")
        return []
