import tweepy, os, time
from dotenv import load_dotenv

load_dotenv()
BEARER = os.getenv("TWITTER_BEARER")

def fetch_twitter(query="OSINT", count=10):
    client = tweepy.Client(bearer_token=BEARER)

    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(count, 100),
            tweet_fields=["created_at", "author_id", "lang"]
        )
    except tweepy.TooManyRequests:
        print("⚠️ Rate limit hit. Waiting 15 minutes...")
        time.sleep(15 * 60)  # wait 15 min
        return fetch_twitter(query, count)

    results = []
    if tweets.data:
        for t in tweets.data:
            results.append({
                "platform": "twitter",
                "user": str(t.author_id),
                "timestamp": str(t.created_at),
                "text": t.text,
                "url": f"https://twitter.com/i/web/status/{t.id}"
            })
    return results
