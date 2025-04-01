from googleapiclient.discovery import build

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
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0)),
            "published_at": item["snippet"]["publishedAt"]
        })
    return videos

# Usage
videos = get_trending_videos("AIzaSyBPNU6Dr2AKfrYhz7KA-ekCBoANtpOrOxI")
