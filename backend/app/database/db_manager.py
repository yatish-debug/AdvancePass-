import sqlite3
import time
import bcrypt
import os
import json
import uuid

DB_PATH = "password_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS logs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   password_hash TEXT,
                   strength TEXT,
                   entropy REAL,
                   crack_time TEXT,
                   timestamp TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS chat_threads (
                   id TEXT PRIMARY KEY,
                   title TEXT,
                   timestamp TEXT,
                   messages_json TEXT)""")
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    # Hash a password for storing.
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password_hash(password: str, hashed: str) -> bool:
    # Check that an unhashed password matches one that has previously been hashed
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def log_to_db(password: str, strength: str, entropy: float, crack_time: str):
    init_db()
    hashed_pwd = hash_password(password)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO logs (password_hash, strength, entropy, crack_time, timestamp) VALUES (?, ?, ?, ?, ?)",
                (hashed_pwd, strength, entropy, crack_time, time.ctime()))
    conn.commit()
    conn.close()

def fetch_previous_hashes():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM logs ORDER BY id DESC LIMIT 100")
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data

def check_password_reuse(password: str) -> bool:
    """Checks if a plaintext password matches any hash in the database."""
    hashes = fetch_previous_hashes()
    for h in hashes:
        if check_password_hash(password, h):
            return True
    return False

def get_statistics():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT strength, COUNT(*) FROM logs GROUP BY strength")
    stats = cur.fetchall()
    conn.close()
    return stats

def get_all_logs():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = [dict(row) for row in cur.fetchall()]
    conn.close()
    return logs

def clear_history():
    """Deletes all records from the logs table."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM logs")
    conn.commit()
    conn.close()

def save_chat_thread(thread_id: str, title: str, messages: list):
    """Saves or updates a chat thread."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    messages_json = json.dumps(messages)
    timestamp = time.ctime()
    
    # Check if exists
    cur.execute("SELECT id FROM chat_threads WHERE id = ?", (thread_id,))
    if cur.fetchone():
        cur.execute("UPDATE chat_threads SET messages_json = ?, timestamp = ? WHERE id = ?", 
                    (messages_json, timestamp, thread_id))
    else:
        cur.execute("INSERT INTO chat_threads (id, title, timestamp, messages_json) VALUES (?, ?, ?, ?)",
                    (thread_id, title, timestamp, messages_json))
    conn.commit()
    conn.close()

def get_all_chat_threads():
    """Retrieves all chat threads ordered by most recent first."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM chat_threads ORDER BY rowid DESC")
    threads = [dict(row) for row in cur.fetchall()]
    # Parse JSON
    for thread in threads:
        thread['messages'] = json.loads(thread['messages_json'])
    conn.close()
    return threads

def delete_chat_thread(thread_id: str):
    """Deletes a specific chat thread."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM chat_threads WHERE id = ?", (thread_id,))
    conn.commit()
    conn.close()
