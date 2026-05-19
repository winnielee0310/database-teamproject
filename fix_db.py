import sqlite3
import sys

db_path = 'c:/Users/User/database-teamproject/idol_trade.db'
conn = sqlite3.connect(db_path, timeout=10)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE Product ADD COLUMN ImageUrl VARCHAR(255)")
    print("Added ImageUrl column")
except Exception as e:
    print(f"Error adding column: {e}")

try:
    cursor.execute("UPDATE Product SET ImageUrl = 'momo.jpeg' WHERE ProductID = 1")
    conn.commit()
    print("Updated Product 1")
except Exception as e:
    print(f"Error updating product: {e}")

conn.close()
