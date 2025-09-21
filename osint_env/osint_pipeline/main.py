import os
from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from utils.cleaner import clean_text, filter_english
from utils.sentiment import add_sentiment
from utils.database import save_to_db, load_from_db

def main():
    data = []

    # Twitter collection
    print("🔎 Collecting tweets from Twitter...")
    tweets = fetch_twitter("OSINT OR cybersecurity", 10)
    
    if tweets:
        tweets = tweets[:5]  # Keep only first 5
        data.extend(tweets)
        print(f"✅ Collected {len(tweets)} Twitter posts")
    else:
        print("❌ Twitter collection failed")

    # Reddit collection
    print("📱 Collecting Reddit posts...")
    reddit_posts = fetch_reddit("osint", 5)
    
    if reddit_posts:
        data.extend(reddit_posts)
        print(f"✅ Collected {len(reddit_posts)} Reddit posts")
    else:
        print("❌ Reddit collection failed")

    if not data:
        print("⚠️ No data collected from any platform. Loading cached data...")
        cached_data = load_from_db()
        if cached_data:
            data.extend(cached_data[:10])  # Load up to 10 cached records
            print(f"📦 Loaded {len(data)} cached records")
        else:
            print("⚠️ No cached data available. Exiting.")
            return

    print("🧹 Filtering English posts...")
    data = filter_english(data)
    
    if not data:
        print("⚠️ No English posts found after filtering")
        return

    print("🧽 Cleaning text...")
    data = clean_text(data)

    print("😊 Adding sentiment...")
    data = add_sentiment(data)

    print("💾 Saving to database...")
    save_to_db(data)

    print(f"✅ Pipeline finished. Collected {len(data)} records from Twitter and Reddit")
    print("\nSample results:")
    for i, r in enumerate(data[:5]):
        print(f"{i+1}. {r['platform']} | {r['user']} | {r['sentiment']:.2f} | {r['text'][:50]}...")

if __name__ == "__main__":
    main()