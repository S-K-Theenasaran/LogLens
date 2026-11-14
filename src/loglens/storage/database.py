
import sqlite3
from pathlib import Path

DB_PATH = Path("data/loglens.db")


def initialize_database():
    """Create the LogLens database and its initial tables."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS log_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                imported_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS log_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER NOT NULL,
                line_number INTEGER,
                timestamp TEXT,
                level TEXT,
                component TEXT,
                message TEXT,
                FOREIGN KEY (file_id) REFERENCES log_files(id)
            );

            CREATE TABLE IF NOT EXISTS parse_failures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id INTEGER NOT NULL,
                line_number INTEGER,
                raw_line TEXT,
                FOREIGN KEY (file_id) REFERENCES log_files(id)
            );
        """)

    print("LogLens database initialized successfully!")


if __name__ == "__main__":
    initialize_database()
