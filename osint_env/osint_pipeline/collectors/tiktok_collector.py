from TikTokApi import TikTokApi
from datetime import datetime
import asyncio

def fetch_tiktok(hashtag="osint", count=5):
    results = []
    try:
        # Initialize TikTokApi
        api = TikTokApi()
        
        # Get hashtag videos - this uses a different approach
        videos = api.hashtag(name=hashtag).videos(count=count)
        
        for video in videos:
            try:
                # Get video details
                video_data = video.info()
                results.append({
                    "platform": "tiktok",
                    "user": video_data['author']['uniqueId'],
                    "timestamp": str(datetime.fromtimestamp(video_data['createTime'])),
                    "text": video_data['desc'],
                    "url": f"https://www.tiktok.com/@{video_data['author']['uniqueId']}/video/{video_data['id']}"
                })
            except Exception as e:
                print(f"❌ Error processing TikTok video: {e}")
                continue
                
    except Exception as e:
        print(f"❌ TikTok API error: {e}")
        # Return empty results if TikTok fails
        return []
    
    return results