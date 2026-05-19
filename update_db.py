import sqlite3

conn = sqlite3.connect('c:/Users/User/database-teamproject/idol_trade.db')
cursor = conn.cursor()

# Get or create group
cursor.execute("SELECT GroupID FROM `Group` WHERE GroupName = 'TWICE'")
group = cursor.fetchone()
if not group:
    cursor.execute("INSERT INTO `Group` (GroupName) VALUES ('TWICE')")
    group_id = cursor.lastrowid
else:
    group_id = group[0]

# Get or create member
cursor.execute("SELECT MemberID FROM Member WHERE MemberName = 'Momo' AND GroupID = ?", (group_id,))
member = cursor.fetchone()
if not member:
    cursor.execute("INSERT INTO Member (MemberName, GroupID) VALUES ('Momo', ?)", (group_id,))
    member_id = cursor.lastrowid
else:
    member_id = member[0]

# Add ImageUrl column if missing
try:
    cursor.execute("ALTER TABLE Product ADD COLUMN ImageUrl VARCHAR(255)")
except sqlite3.OperationalError:
    pass

# Update product 1
cursor.execute("UPDATE Product SET Price = 350, ImageUrl = 'momo.jpg' WHERE ProductID = 1")
cursor.execute("DELETE FROM Product_Member_Rel WHERE ProductID = 1")
cursor.execute("INSERT INTO Product_Member_Rel (ProductID, MemberID) VALUES (1, ?)", (member_id,))

conn.commit()
conn.close()
print('Success')
