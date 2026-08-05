import sqlite3
from pathlib import Path

# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FOLDER = BASE_DIR / "database"

DB_FOLDER.mkdir(exist_ok=True)

DB_PATH = DB_FOLDER / "users.db"


# --------------------------------------------------
# Get Database Connection
# --------------------------------------------------

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# --------------------------------------------------
# Create Users Table
# --------------------------------------------------

def create_users_table():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()

    conn.close()


# --------------------------------------------------
# Add User
# --------------------------------------------------

def add_user(
    full_name,
    username,
    password,
    role="Analyst"
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (full_name, username, password, role)
        VALUES (?, ?, ?, ?)
        """,
        (
            full_name,
            username,
            password,
            role
        )
    )

    conn.commit()

    conn.close()


# --------------------------------------------------
# Get User
# --------------------------------------------------

def get_user(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# --------------------------------------------------
# Get All Users
# --------------------------------------------------

def get_all_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            full_name,
            username,
            role,
            created_at
        FROM users
        """
    )

    users = cursor.fetchall()

    conn.close()

    return users


# --------------------------------------------------
# Delete User
# --------------------------------------------------

def delete_user(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM users
        WHERE id=?
        """,
        (user_id,)
    )

    conn.commit()

    conn.close()


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

def initialize_database():

    create_users_table()


# --------------------------------------------------
# Run Directly
# --------------------------------------------------

if __name__ == "__main__":

    initialize_database()

    print("Database initialized successfully.")