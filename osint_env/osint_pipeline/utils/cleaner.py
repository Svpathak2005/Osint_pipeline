from langdetect import detect

def filter_english(records):
    cleaned = []
    for r in records:
        text = r.get("text")
        if text and isinstance(text, str):
            try:
                if detect(text) == "en":
                    cleaned.append(r)
            except:
                continue
    return cleaned

def clean_text(records):
    cleaned = []
    for r in records:
        text = r.get("text")
        if text:
            # Remove URLs
            text = ' '.join(word for word in text.split() if not word.startswith('http'))
            # Remove special characters but keep basic punctuation
            text = ' '.join(word for word in text.split() if not word.startswith('@') and not word.startswith('#'))
            # Replace newlines with spaces
            r["text"] = text.strip().replace("\n", " ")
            cleaned.append(r)
    return cleaned