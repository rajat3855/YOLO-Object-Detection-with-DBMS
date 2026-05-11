import sqlite3

def init_db():
    conn = sqlite3.connect("detections.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            labels TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_detection(filename: str, labels: list):
    conn = sqlite3.connect("detections.db")
    conn.execute(
        "INSERT INTO detections (filename, labels) VALUES (?, ?)",
        (filename, str(labels))
    )
    conn.commit()
    conn.close()

def get history():
    conn = sqlite3.connect("detections.db")
    rows = conn.execute(
        "SELECT * FROM detections ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return rows
