import praw
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def fetch_reddit(subreddit="osint", limit=10):
    """
    Fetch posts from a Reddit subreddit using read-only access
    """
    # Check if we have the required credentials
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("⚠️ Reddit API credentials not found. Using mock data.")
        return mock_reddit_data(subreddit, limit)
    
    results = []
    
    try:
        # Use read-only access (no user authentication needed)
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="osint_pipeline/1.0 by sumect2005"
        )
        
        # Set read-only mode
        reddit.read_only = True
        
        # Fetch posts from the subreddit
        print(f"📱 Fetching posts from r/{subreddit}...")
        subreddit_obj = reddit.subreddit(subreddit)
        
        for post in subreddit_obj.hot(limit=limit):
            # Skip stickied posts (usually rules/announcements)
            if post.stickied:
                continue
                
            # Convert timestamp to readable format
            post_time = datetime.fromtimestamp(post.created_utc)
            
            # Clean text - combine title and body
            text_content = post.title
            if post.selftext:  # If post has body text
                text_content += " - " + post.selftext
                
            results.append({
                "platform": "reddit",
                "user": str(post.author) if post.author else "Unknown",
                "timestamp": str(post_time),
                "text": text_content,
                "url": f"https://www.reddit.com{post.permalink}"
            })
            
    except Exception as e:
        print(f"❌ Reddit API error: {e}")
        return mock_reddit_data(subreddit, limit)
    
    return results

def mock_reddit_data(subreddit="osint", limit=10):
    """
    Mock Reddit data for testing when API fails
    """
    from datetime import datetime, timedelta
    import random
    
    print("⚠️ Using mock Reddit data")
    
    mock_titles = [
        f"Great OSINT resource found in r/{subreddit}",
        f"Discussion about digital forensics in r/{subreddit}",
        f"New OSINT tools review in r/{subreddit}",
        f"Case study shared in r/{subreddit}",
        f"Question about investigation techniques in r/{subreddit}"
    ]
    
    mock_users = ["osint_expert", "digital_detective", "cyber_researcher", "data_sleuth", "info_gatherer"]
    
    results = []
    for i in range(min(limit, 5)):
        results.append({
            "platform": "reddit",
            "user": random.choice(mock_users),
            "timestamp": str(datetime.now() - timedelta(hours=random.randint(1, 24))),
            "text": random.choice(mock_titles),
            "url": f"https://www.reddit.com/r/{subreddit}/comments/mock_post_{i}"
        })
    
    return results