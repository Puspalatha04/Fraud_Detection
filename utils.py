import sqlite3
import hashlib
import streamlit as st # Only needed for st.error, consider logging or raising instead for pure utility

# --- Database Functions ---
DB_FILE = 'app_data.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This enables access to columns by name
    return conn

def initialize_database():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                raw_input TEXT NOT NULL,
                prediction TEXT NOT NULL,
                probability REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        ''')

        conn.commit()
    except sqlite3.Error as e:
        # In a utility file, it's better to log this or propagate the error
        # For Streamlit apps, st.error might be acceptable if directly called from app context
        st.error(f"Database error during initialization: {e}")
    finally:
        if conn:
            conn.close()

def create_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user

def reset_user_password(username, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    try:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_exists = cursor.fetchone()
        if user_exists:
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_password_hash, username))
            conn.commit()
            return True
        else:
            st.error("Username not found.")
            return False
    except sqlite3.Error as e:
        st.error(f"Database error during password reset: {e}")
        return False
    finally:
        conn.close()
