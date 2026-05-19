import sqlite3
try:
    conn = sqlite3.connect('c:/Users/User/database-teamproject/idol_trade.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Product")
    cursor.execute("DELETE FROM Product_Member_Rel")
    cursor.execute("DELETE FROM `Order`")
    cursor.execute("DELETE FROM Review")
    conn.commit()
    conn.close()
    print("Successfully cleared mock products!")
except Exception as e:
    print("Error:", e)
