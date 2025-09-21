import tweepy, os
import time
from dotenv import load_dotenv

load_dotenv()
BEARER = os.getenv("TWITTER_BEARER")

def fetch_twitter(query="OSINT", count=10, max_retries=3):
    """
    Fetch tweets from Twitter API with retry logic
    """
    # If no bearer token, use mock data
    if not BEARER:
        print("⚠️ Twitter bearer token not found. Using mock data.")
        return mock_twitter_data(query, count)
    
    client = tweepy.Client(bearer_token=BEARER)
    safe_count = max(10, min(count, 100))
    
    for attempt in range(max_retries):
        try:
            tweets = client.search_recent_tweets(
                query=query,
                max_results=safe_count,
                tweet_fields=["created_at", "author_id", "lang"]
            )
            
            results = []
            if tweets and tweets.data:
                for t in tweets.data:
                    results.append({
                        "platform": "twitter",
                        "user": str(t.author_id),
                        "timestamp": str(t.created_at),
                        "text": t.text,
                        "url": f"https://twitter.com/i/web/status/{t.id}"
                    })
            return results
            
        except tweepy.errors.TooManyRequests:
            if attempt < max_retries - 1:
                wait_time = 60 * (attempt + 1)
                print(f"⚠️ Twitter rate limited. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
            else:
                print("❌ Max retries exceeded. Returning empty Twitter results.")
                return []
                
        except Exception as e:
            print(f"❌ Twitter API error: {e}")
            return mock_twitter_data(query, count)

def mock_twitter_data(query="OSINT", count=5):
    """
    Mock Twitter data for testing when API fails
    """
    from datetime import datetime, timedelta
    import random
    
    print("⚠️ Using mock Twitter data")
    
    mock_texts = [
        f"Interesting findings about {query} #OSINT",
        f"New {query} techniques discovered today",
        f"Case study: Using {query} in digital investigations",
        f"How {query} is changing the cybersecurity landscape",
        f"Resources for learning more about {query}"
    ]
    
    mock_users = ["123456789", "987654321", "456789123", "789123456", "321654987"]
    
    results = []
    for i in range(min(count, 5)):
        results.append({
            "platform": "twitter",
            "user": random.choice(mock_users),
            "timestamp": str(datetime.now() - timedelta(hours=random.randint(1, 24))),
            "text": random.choice(mock_texts),
            "url": f"https://twitter.com/i/web/status/{random.randint(1000000000, 9999999999)}"
        })
    
    return results