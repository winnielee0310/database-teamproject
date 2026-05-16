import sqlite3
import os

DB_PATH = "../idol_trade.db"
SCHEMA_PATH = "../schema.sql"
DATA_PATH = "../insert_data.sql"

def setup_database():
    # 若舊的 DB 存在先刪除，確保乾淨環境
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 執行 DDL 建立表格
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_script = f.read()
        cursor.executescript(schema_script)
        print("✅ 成功建立資料庫 Schema")
        
    # 執行 DML 插入測試資料
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data_script = f.read()
        cursor.executescript(data_script)
        print("✅ 成功插入模擬測試資料")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
