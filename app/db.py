import os
import sqlite3
from pathlib import Path


def get_db_path() -> str:
    return os.getenv("DATABASE_PATH", str(Path(__file__).resolve().parent.parent / "app.db"))


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(get_db_path())
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    con = connect()
    try:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        con.commit()
    finally:
        con.close()
