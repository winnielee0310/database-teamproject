import sqlite3
import re

# 1. Update Database Schema
conn = sqlite3.connect('c:/Users/User/database-teamproject/idol_trade.db', timeout=10)
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE Product RENAME COLUMN Condition TO ProductName")
    print("Renamed Condition to ProductName")
except Exception as e:
    print(e)
try:
    cursor.execute("ALTER TABLE Product ADD COLUMN Description TEXT")
    print("Added Description column")
except Exception as e:
    print(e)
conn.commit()
conn.close()

# 2. Update models.py
with open('c:/Users/User/database-teamproject/backend/models.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Condition = Column(String(50), nullable=False)", "ProductName = Column(String(100), nullable=False)\n    Description = Column(Text, nullable=True)")
with open('c:/Users/User/database-teamproject/backend/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Update schemas.py
with open('c:/Users/User/database-teamproject/backend/schemas.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Condition: str", "ProductName: str\n    Description: Optional[str] = None")
with open('c:/Users/User/database-teamproject/backend/schemas.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 4. Update main.py
with open('c:/Users/User/database-teamproject/backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Condition=product.Condition", "ProductName=product.ProductName, Description=product.Description")
content = content.replace('"Condition": p.Condition', '"ProductName": p.ProductName, "Description": p.Description')
with open('c:/Users/User/database-teamproject/backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 5. Update index.html
with open('c:/Users/User/database-teamproject/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace sell form inputs
sell_html_old = """                    <div class="form-group">
                        <label>商品卡況 (如：全新、微損)</label>
                        <input type="text" id="sell-condition" placeholder="請描述卡片保存狀況" required>
                    </div>"""
sell_html_new = """                    <div class="form-group">
                        <label>商品名稱</label>
                        <input type="text" id="sell-name" placeholder="例如：The Name Chapter 專卡" required>
                    </div>
                    <div class="form-group" style="grid-column: 1 / -1;">
                        <label>商品描述</label>
                        <textarea id="sell-desc" placeholder="請詳細描述商品狀況、是否拆封等..." rows="3" style="width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--border); font-family: inherit; resize: vertical;"></textarea>
                    </div>"""
content = content.replace(sell_html_old, sell_html_new)

# Replace modal details
detail_html_old = """                    <p style="margin-bottom: 10px;"><strong style="color: var(--primary);">商品卡況：</strong> <span id="detail-condition"></span></p>"""
detail_html_new = """                    <p style="margin-bottom: 10px;"><strong style="color: var(--primary);">商品名稱：</strong> <span id="detail-name"></span></p>
                    <p style="margin-bottom: 10px;"><strong style="color: var(--primary);">商品描述：</strong> <span id="detail-desc"></span></p>"""
content = content.replace(detail_html_old, detail_html_new)

with open('c:/Users/User/database-teamproject/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated backend and HTML logic successfully")
