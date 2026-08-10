"""
Auth helpers using bcrypt and sqlite3.

Functions:
- create_user(conn, username, password) -> bool (False if user exists)
- verify_user(conn, username, password) -> bool
- user_exists(conn, username) -> bool
"""
import sqlite3
import bcrypt

def user_exists(conn: sqlite3.Connection, username: str) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return cur.fetchone() is not None

def create_user(conn: sqlite3.Connection, username: str, password: str) -> bool:
    if user_exists(conn, username):
        return False
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, pw_hash)
    )
    conn.commit()
    return True

def verify_user(conn: sqlite3.Connection, username: str, password: str) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return False
    stored = row[0]
    # stored is bytes if read from sqlite as BLOB, or str; ensure bytes
    if isinstance(stored, str):
        stored = stored.encode("utf-8")
    try:
        return bcrypt.checkpw(password.encode("utf-8"), stored)
    except ValueError:
        return False
