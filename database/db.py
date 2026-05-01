import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "spendly.db"


def get_db():
    """Open connection to SQLite database with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create database tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def get_user_by_email(email):
    """Fetch user by email. Returns None if not found."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def verify_user_password(email, password):
    """Verify user password. Returns user dict if valid, None if invalid."""
    from werkzeug.security import check_password_hash

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def create_user(name, email, password):
    """Create new user with hashed password. Returns new user ID."""
    conn = get_db()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return user_id


def seed_db():
    """Insert demo data if not already present."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user
    password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash)
    )

    # Get the demo user's ID
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@spendly.com",))
    user_id = cursor.fetchone()[0]

    # Insert 8 sample expenses across all categories
    expenses = [
        (user_id, 45.50, "Food", "2026-04-01", "Lunch at cafe"),
        (user_id, 25.00, "Transport", "2026-04-03", "Uber ride"),
        (user_id, 120.00, "Bills", "2026-04-05", "Electric bill"),
        (user_id, 35.00, "Health", "2026-04-07", "Pharmacy"),
        (user_id, 50.00, "Entertainment", "2026-04-10", "Movie tickets"),
        (user_id, 89.99, "Shopping", "2026-04-12", "New shirt"),
        (user_id, 15.00, "Other", "2026-04-15", "Miscellaneous"),
        (user_id, 65.00, "Food", "2026-04-18", "Dinner with friends"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )

    conn.commit()
    conn.close()
