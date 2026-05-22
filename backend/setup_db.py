import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DB_PATH = PROJECT_DIR / "idol_trade.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"
DATA_PATH = BASE_DIR / "insert_data.sql"


def setup_database() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"Removed existing database: {DB_PATH}")

    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        schema_script = file.read()

    with DATA_PATH.open("r", encoding="utf-8") as file:
        data_script = file.read()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(schema_script)
        print("Created database schema.")

        conn.executescript(data_script)
        print("Inserted demo data.")

    print(f"Database ready: {DB_PATH}")


if __name__ == "__main__":
    setup_database()
