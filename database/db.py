import os
import sqlite3
from datetime import date, timedelta

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "expense_tracker.db")
DB_PATH = os.path.abspath(DB_PATH)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        count = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
        if count > 0:
            return

        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cursor.lastrowid

        first_of_month = date.today().replace(day=1)
        offsets = [1, 3, 5, 7, 10, 13, 16, 19]

        expenses = [
            (user_id, 45.50, "Food",         str(first_of_month + timedelta(days=offsets[0])), "Grocery shopping"),
            (user_id, 12.00, "Transport",     str(first_of_month + timedelta(days=offsets[1])), "Bus fare"),
            (user_id, 89.99, "Bills",         str(first_of_month + timedelta(days=offsets[2])), "Electricity bill"),
            (user_id, 25.00, "Health",        str(first_of_month + timedelta(days=offsets[3])), "Pharmacy"),
            (user_id, 15.50, "Entertainment", str(first_of_month + timedelta(days=offsets[4])), "Movie ticket"),
            (user_id, 60.00, "Shopping",      str(first_of_month + timedelta(days=offsets[5])), "New shoes"),
            (user_id,  8.75, "Other",         str(first_of_month + timedelta(days=offsets[6])), "Miscellaneous"),
            (user_id, 32.20, "Food",          str(first_of_month + timedelta(days=offsets[7])), "Restaurant dinner"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses,
        )
        conn.commit()
    finally:
        conn.close()
