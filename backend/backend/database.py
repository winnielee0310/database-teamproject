from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 這裡使用 SQLite 作為本地資料庫測試，您可以根據需求替換為 MySQL 或 PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite:///../idol_trade.db"

# 啟用 SQLite 的外鍵支持
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
