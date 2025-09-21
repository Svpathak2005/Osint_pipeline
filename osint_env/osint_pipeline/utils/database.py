import sqlite3

def save_to_db(records, db_name="osint.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS data (
        platform TEXT,
        user TEXT,
        timestamp TEXT,
        text TEXT,
        url TEXT,
        sentiment REAL
    )""")

    for r in records:
        c.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)", (
            r.get("platform"),
            r.get("user"),
            r.get("timestamp"),
            r.get("text"),
            r.get("url"),
            r.get("sentiment", 0)
        ))

    conn.commit()
    conn.close()


def load_from_db(db_name="osint.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Check table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
    if not c.fetchone():
        conn.close()
        return []

    c.execute("SELECT platform, user, timestamp, text, url, sentiment FROM data ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    return [
        {
            "platform": r[0],
            "user": r[1],
            "timestamp": r[2],
            "text": r[3],
            "url": r[4],
            "sentiment": r[5]
        }
        for r in rows
    ]