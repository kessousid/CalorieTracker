import sqlite3
import os
import hashlib
import secrets
from datetime import date

_DATA_DIR = os.path.join(os.path.expanduser("~"), ".calorie_tracker_data")
os.makedirs(_DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(_DATA_DIR, "calorie_tracker.db")

# Schema version: bump when tables change incompatibly
SCHEMA_VERSION = 4


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_meta (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        row = conn.execute(
            "SELECT value FROM schema_meta WHERE key='version'"
        ).fetchone()
        current = int(row[0]) if row else 0

        if current < SCHEMA_VERSION:
            _migrate(conn, current)
            conn.execute("""
                INSERT OR REPLACE INTO schema_meta (key, value)
                VALUES ('version', ?)
            """, (str(SCHEMA_VERSION),))
        conn.commit()


def _migrate(conn, from_version: int):
    if from_version < 3:
        # Drop old tables that lack user_id — data from v1/v2 is discarded
        conn.execute("DROP TABLE IF EXISTS food_log")
        conn.execute("DROP TABLE IF EXISTS daily_settings")
        conn.execute("DROP TABLE IF EXISTS users")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL COLLATE NOCASE,
            email TEXT UNIQUE NOT NULL COLLATE NOCASE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            default_target INTEGER NOT NULL DEFAULT 2000,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    if from_version < 4:
        # Add health profile columns non-destructively
        for col_def in [
            "age INTEGER",
            "weight_kg REAL",
            "height_cm REAL",
            "sex TEXT",
            "activity_level TEXT",
            "calorie_need INTEGER",
        ]:
            try:
                conn.execute(f"ALTER TABLE users ADD COLUMN {col_def}")
            except Exception:
                pass  # column already exists

    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_settings (
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            calorie_target INTEGER NOT NULL DEFAULT 2000,
            PRIMARY KEY (user_id, date),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS food_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            meal_period TEXT NOT NULL,
            food_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            calories_per_unit REAL NOT NULL,
            total_calories REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_food_log_user_date ON food_log(user_id, date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_settings_user_date ON daily_settings(user_id, date)")


# ─── Password helpers ─────────────────────────────────────────────────────────

def _hash_password(password: str) -> tuple[str, str]:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return key.hex(), salt


def _verify_password(password: str, stored_hash: str, salt: str) -> bool:
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return secrets.compare_digest(key.hex(), stored_hash)


# ─── User auth ────────────────────────────────────────────────────────────────

def register_user(name: str, username: str, email: str,
                  password: str, default_target: int = 2000,
                  age: int | None = None, weight_kg: float | None = None,
                  height_cm: float | None = None, sex: str | None = None,
                  activity_level: str | None = None,
                  calorie_need: int | None = None) -> tuple[bool, str]:
    """Returns (success, message)."""
    pw_hash, salt = _hash_password(password)
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO users
                    (name, username, email, password_hash, salt, default_target,
                     age, weight_kg, height_cm, sex, activity_level, calorie_need)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name.strip(), username.strip(), email.strip().lower(),
                  pw_hash, salt, default_target,
                  age, weight_kg, height_cm, sex, activity_level, calorie_need))
            conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError as e:
        if "username" in str(e).lower():
            return False, "Username already taken. Please choose another."
        if "email" in str(e).lower():
            return False, "An account with this email already exists."
        return False, "Registration failed. Please try again."


def verify_user(username: str, password: str) -> dict | None:
    """Returns user dict on success, None on failure."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, name, username, email, password_hash, salt, default_target
            FROM users WHERE username = ?
        """, (username.strip(),)).fetchone()
    if row and _verify_password(password, row[4], row[5]):
        return {
            "id": row[0], "name": row[1], "username": row[2],
            "email": row[3], "default_target": row[6],
        }
    return None


def get_user_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, name, username, email, default_target
            FROM users WHERE id = ?
        """, (user_id,)).fetchone()
    if row:
        return {"id": row[0], "name": row[1], "username": row[2],
                "email": row[3], "default_target": row[4]}
    return None


def update_default_target(user_id: int, target: int):
    with get_connection() as conn:
        conn.execute("UPDATE users SET default_target = ? WHERE id = ?", (target, user_id))
        conn.commit()


def update_password(user_id: int, new_password: str) -> bool:
    pw_hash, salt = _hash_password(new_password)
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ?, salt = ? WHERE id = ?",
            (pw_hash, salt, user_id)
        )
        conn.commit()
    return True


# ─── Daily Settings ───────────────────────────────────────────────────────────

def set_daily_target(user_id: int, target_date: str, target: int):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO daily_settings (user_id, date, calorie_target)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET calorie_target = excluded.calorie_target
        """, (user_id, target_date, target))
        conn.commit()


def get_daily_target(user_id: int, target_date: str) -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT calorie_target FROM daily_settings WHERE user_id = ? AND date = ?",
            (user_id, target_date)
        ).fetchone()
        if row:
            return row[0]
        # Fall back to the user's default target
        default = conn.execute(
            "SELECT default_target FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return default[0] if default else 2000


# ─── Food Log ─────────────────────────────────────────────────────────────────

def add_food_entry(user_id: int, log_date: str, meal_period: str,
                   food_name: str, quantity: float, unit: str,
                   calories_per_unit: float) -> float:
    total = round(quantity * calories_per_unit, 1)
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO food_log
                (user_id, date, meal_period, food_name, quantity, unit,
                 calories_per_unit, total_calories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, log_date, meal_period, food_name,
              quantity, unit, calories_per_unit, total))
        conn.commit()
    return total


def delete_food_entry(entry_id: int, user_id: int):
    """Delete only if it belongs to this user."""
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM food_log WHERE id = ? AND user_id = ?",
            (entry_id, user_id)
        )
        conn.commit()


def get_food_log(user_id: int, log_date: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, meal_period, food_name, quantity, unit,
                   calories_per_unit, total_calories
            FROM food_log
            WHERE user_id = ? AND date = ?
            ORDER BY id
        """, (user_id, log_date)).fetchall()
    return [
        {
            "id": r[0], "meal_period": r[1], "food_name": r[2],
            "quantity": r[3], "unit": r[4],
            "calories_per_unit": r[5], "total_calories": r[6],
        }
        for r in rows
    ]


def get_meal_totals(user_id: int, log_date: str) -> dict:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT meal_period, SUM(total_calories)
            FROM food_log
            WHERE user_id = ? AND date = ?
            GROUP BY meal_period
        """, (user_id, log_date)).fetchall()
    return {r[0]: round(r[1], 1) for r in rows}


def get_daily_total(user_id: int, log_date: str) -> float:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT COALESCE(SUM(total_calories), 0)
            FROM food_log WHERE user_id = ? AND date = ?
        """, (user_id, log_date)).fetchone()
    return round(row[0], 1)


def get_weekly_summary(user_id: int, reference_date: str) -> list[dict]:
    """Return per-day totals for the 7 days ending on reference_date."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT date, SUM(total_calories) AS total
            FROM food_log
            WHERE user_id = ?
              AND date <= ?
              AND date >= DATE(?, '-6 days')
            GROUP BY date
            ORDER BY date
        """, (user_id, reference_date, reference_date)).fetchall()
    return [{"date": r[0], "total": round(r[1], 1)} for r in rows]
