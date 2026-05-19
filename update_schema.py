import sqlite3
import os

# 1. Drop Message table
try:
    conn = sqlite3.connect('c:/Users/User/database-teamproject/idol_trade.db', timeout=10)
    conn.execute("DROP TABLE Message")
    conn.commit()
    conn.close()
    print("Dropped old Message table.")
except Exception as e:
    print("Drop table error:", e)

# 2. Update models.py
with open('c:/Users/User/database-teamproject/backend/models.py', 'r', encoding='utf-8') as f:
    content = f.read()
if "MediaUrl" not in content:
    content = content.replace(
        "Content = Column(Text, nullable=False)",
        "Content = Column(Text, nullable=False)\n    MediaUrl = Column(String(255), nullable=True)"
    )
    with open('c:/Users/User/database-teamproject/backend/models.py', 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Update schemas.py
with open('c:/Users/User/database-teamproject/backend/schemas.py', 'r', encoding='utf-8') as f:
    content = f.read()
if "MediaUrl" not in content:
    content = content.replace(
        "Content: str\n\nclass MessageResponse",
        "Content: str\n    MediaUrl: Optional[str] = None\n\nclass MessageResponse"
    )
    content = content.replace(
        "SentAt: datetime",
        "SentAt: datetime\n    MediaUrl: Optional[str] = None"
    )
    with open('c:/Users/User/database-teamproject/backend/schemas.py', 'w', encoding='utf-8') as f:
        f.write(content)

print("Schema updated successfully")
