from textblob import TextBlob

def add_sentiment(records):
    for r in records:
        text = r.get("text")
        if text:
            r["sentiment"] = TextBlob(text).sentiment.polarity
        else:
            r["sentiment"] = 0
    return records