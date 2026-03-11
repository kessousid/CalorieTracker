import sqlite3
import os
from datetime import date

_DATA_DIR = os.path.join(os.path.expanduser("~"), ".calorie_tracker_data")
os.makedirs(_DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(_DATA_DIR, "calorie_tracker.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_settings (
                date TEXT PRIMARY KEY,
                calorie_target INTEGER NOT NULL DEFAULT 2000
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS food_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                meal_period TEXT NOT NULL,
                food_name TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                calories_per_unit REAL NOT NULL,
                total_calories REAL NOT NULL
            )
        """)
        conn.commit()


# ─── Daily Settings ───────────────────────────────────────────────────────────

def set_daily_target(target_date: str, target: int):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO daily_settings (date, calorie_target)
            VALUES (?, ?)
            ON CONFLICT(date) DO UPDATE SET calorie_target = excluded.calorie_target
        """, (target_date, target))
        conn.commit()


def get_daily_target(target_date: str) -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT calorie_target FROM daily_settings WHERE date = ?", (target_date,)
        ).fetchone()
    return row[0] if row else 2000


# ─── Food Log ─────────────────────────────────────────────────────────────────

def add_food_entry(log_date: str, meal_period: str, food_name: str,
                   quantity: float, unit: str, calories_per_unit: float):
    total = round(quantity * calories_per_unit, 1)
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO food_log (date, meal_period, food_name, quantity, unit,
                                  calories_per_unit, total_calories)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (log_date, meal_period, food_name, quantity, unit, calories_per_unit, total))
        conn.commit()
    return total


def delete_food_entry(entry_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM food_log WHERE id = ?", (entry_id,))
        conn.commit()


def get_food_log(log_date: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, meal_period, food_name, quantity, unit,
                   calories_per_unit, total_calories
            FROM food_log
            WHERE date = ?
            ORDER BY id
        """, (log_date,)).fetchall()
    return [
        {
            "id": r[0], "meal_period": r[1], "food_name": r[2],
            "quantity": r[3], "unit": r[4],
            "calories_per_unit": r[5], "total_calories": r[6]
        }
        for r in rows
    ]


def get_meal_totals(log_date: str) -> dict:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT meal_period, SUM(total_calories)
            FROM food_log
            WHERE date = ?
            GROUP BY meal_period
        """, (log_date,)).fetchall()
    return {r[0]: round(r[1], 1) for r in rows}


def get_daily_total(log_date: str) -> float:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT COALESCE(SUM(total_calories), 0)
            FROM food_log WHERE date = ?
        """, (log_date,)).fetchone()
    return round(row[0], 1)


def get_weekly_summary(reference_date: str) -> list[dict]:
    """Return last 7 days of totals relative to reference_date."""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT date, SUM(total_calories) as total
            FROM food_log
            WHERE date <= ? AND date >= DATE(?, '-6 days')
            GROUP BY date
            ORDER BY date
        """, (reference_date, reference_date)).fetchall()
    return [{"date": r[0], "total": round(r[1], 1)} for r in rows]
