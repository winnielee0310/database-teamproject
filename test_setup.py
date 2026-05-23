import sqlite3
from pathlib import Path

from setup_db import DB_PATH, setup_database


REQUIRED_TABLES = {
    "User",
    "Group",
    "Member",
    "Product",
    "Product_Member_Rel",
    "Order",
    "Wishlist",
    "Review",
    "ProductMessage",
    "Chat",
    "ChatMessage",
}


def main() -> None:
    setup_database()

    if not Path(DB_PATH).exists():
        raise SystemExit(f"Database was not created: {DB_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        missing = REQUIRED_TABLES - tables
        if missing:
            raise SystemExit(f"Missing tables: {', '.join(sorted(missing))}")

        product_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(Product)")
        }
        for column in ("商品名稱", "商品描述", "商品狀況", "圖片網址"):
            if column not in product_columns:
                raise SystemExit(f"Product table is missing column: {column}")

        product_count = conn.execute("SELECT COUNT(*) FROM Product").fetchone()[0]
        user_count = conn.execute("SELECT COUNT(*) FROM User").fetchone()[0]
        available_count = conn.execute(
            "SELECT COUNT(*) FROM Product WHERE `狀態` = 'Available'"
        ).fetchone()[0]

    print(f"Users: {user_count}")
    print(f"Products: {product_count}")
    print(f"Available products: {available_count}")
    print("Database setup test passed.")


if __name__ == "__main__":
    main()
