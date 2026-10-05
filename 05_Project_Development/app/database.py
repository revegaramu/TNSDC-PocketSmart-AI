import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.config import settings


def _database_path() -> str:
    path = Path(settings.DATABASE_PATH)

    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)

    return str(path)


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(
        _database_path(),
        timeout=30,
    )
    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db() -> None:
    with get_db() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                input_json TEXT NOT NULL,
                result_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_recommendations_user
            ON recommendations(user_id, id DESC);
            """
        )


def create_user(
    name: str,
    email: str,
    password_hash: str,
) -> int:
    with get_db() as db:
        cursor = db.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name, email.lower(), password_hash),
        )
        return int(cursor.lastrowid)


def get_user_by_email(email: str):
    with get_db() as db:
        return db.execute(
            "SELECT * FROM users WHERE email = ? COLLATE NOCASE",
            (email.lower(),),
        ).fetchone()


def get_user_by_id(user_id: int):
    with get_db() as db:
        return db.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()


def save_recommendation(
    user_id: int,
    category: str,
    input_json: str,
    result_json: str,
) -> int:
    with get_db() as db:
        cursor = db.execute(
            """
            INSERT INTO recommendations
                (user_id, category, input_json, result_json)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, category, input_json, result_json),
        )
        return int(cursor.lastrowid)


def get_recommendations(user_id: int, limit: int = 20):
    with get_db() as db:
        return db.execute(
            """
            SELECT id, category, input_json, result_json, created_at
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()


def count_recommendations(user_id: int) -> int:
    with get_db() as db:
        row = db.execute(
            """
            SELECT COUNT(*) AS total
            FROM recommendations
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        return int(row["total"])