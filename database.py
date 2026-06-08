import sqlite3
import hashlib
import os

DB_NAME = "users_database.db"

def get_db_connection():
    """Creates and returns a connection to the database."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def hash_password(password):
    """Hashes a password using SHA-256 with a salt."""
    salt = "spd_project_salt" 
    return hashlib.sha256((password + salt).encode()).hexdigest()

def create_users_table():
    """Creates the users table and adds default users."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('SELECT count(*) FROM users')
    if cursor.fetchone()[0] == 0:
        users = {
            "angel.garcia": "12345", 
            "shaine.eceja": "12345",
            "lovely.serafica": "12345"
        }
        for u, p in users.items():
            hashed = hash_password(p)
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, hashed))
            except: pass
            
    conn.commit()
    conn.close()

def register_user(username, password):
    """Registers a new user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
    except: pass
    finally: conn.close()

def authenticate_user(username, password):
    """Checks credentials."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0] == hash_password(password):
            return True
    except: return False
    return False

def get_user_details(username):
    """Returns user details (needed by main.py)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user