import sqlite3
import hashlib
import json
from datetime import datetime

class SimpleCache:
    def __init__(self, path="cache.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init_table()

    def _init_table(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            id TEXT PRIMARY KEY,
            key TEXT,
            text TEXT,
            value TEXT,
            embedding TEXT,
            last_used TEXT,
            use_count INTEGER
        )
        """)
        self.conn.commit()

    def save(self, text, embedding, value):
        key = hashlib.sha256(text.encode()).hexdigest()

        cur = self.conn.cursor()
        cur.execute(
            """INSERT OR REPLACE INTO cache 
               (id, key, text, value, embedding, last_used, use_count)
               VALUES (?,?,?,?,?,?,?)""",
            (
                key,
                key,
                text,
                json.dumps(value),
                json.dumps(embedding),
                datetime.utcnow().isoformat(),
                1,
            ),
        )
        self.conn.commit()

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT text, value, embedding FROM cache")
        rows = cur.fetchall()

        results = []
        for text, value, embedding in rows:
            results.append({
                "text": text,
                "value": json.loads(value),
                "embedding": json.loads(embedding)
            })
        return results
