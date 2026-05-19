import sqlite3

conn = sqlite3.connect('c:/Users/User/database-teamproject/idol_trade.db')
cursor = conn.cursor()
cursor.execute("UPDATE Product SET ImageUrl = 'momo.jpeg' WHERE ProductID = 1")
conn.commit()
conn.close()
print('Success')
