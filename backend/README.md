# 偶像周邊二手交易與訂單管理系統 (Idol Merchandise Trading System)

本專案為**國立高雄師範大學 軟體工程與管理學系 114-2 學年度資料庫期末報告計劃**之實作系統。專門針對粉絲在購買、交換與轉售偶像周邊商品（如專輯、小卡、應援物等）的行為，設計的一套具備完整資料管理與交易流程的關聯式資料庫系統。

## 🌟 系統亮點特色
1. **多成員關聯檢索 (解決 N:M 問題)**：捨棄傳統社群純文字的雜亂檢索。透過嚴謹的 `Product_Member_Rel` 關聯表，精準檢索包含該成員的所有單人卡與多人卡（如雙人卡、小分隊卡）。
2. **願望清單需求撮合 (貨找人)**：買家可設定預算與特定成員，系統會在商品上架時自動撈取並比對符合條件的買家清單。
3. **悲觀鎖防超賣機制**：針對限量絕版小卡的搶購情境，訂單結帳流程採用 `SELECT ... FOR UPDATE` 悲觀鎖，確保交易一致性。
4. **專屬信譽評估模型**：捨棄傳統單一評分，專門為偶像圈設計了「包裝保護度」、「對光錄影確認」、「出貨速度」三維度評分，並透過 SQL 聚合查詢動態計算賣家信譽。

## 📊 ERD 實體關係對應與 API 實作
根據專案的**實體關係圖 (ERD)**，本後端已將圖中所有的**實體 (Entities)** 與**關係 (Relationships)** 轉換為對應的資料表與完整的 CRUD API：

1. **使用者 (User)**：包含註冊與登入資訊，具備 `1:N` 購買/販售/設定願望清單之關係。對應 API：`POST /users/`。
2. **團體與成員 (Group & Member)**：團體 `1:N` 包含成員。對應 API：`GET /groups/`、`GET /groups/{id}/members`。
3. **商品 (Product) 與標記成員**：為了解決 ERD 中商品與成員的 **多對多 (N:M)** 關係，我們實作了 `Product_Member_Rel` 關聯表。對應 API：`POST /products/` 與 `GET /products/search`。
4. **願望清單 (Wishlist)**：記錄 User 追蹤特定 Member 周邊的需求 (`N:1`)。對應 API：`POST /wishlists/`、`GET /users/{id}/wishlists`。
5. **訂單與評價 (Order & Review)**：一筆訂單對應一項商品 (`1:1`)，並可產生一筆專屬評價 (`1:1`)。對應 API：`POST /orders/` 與 `POST /reviews/`。

## 📂 專案架構
```text
database-teamproject/
├── README.md               # 專案介紹
├── schema.sql              # 資料庫 DDL (表格、約束定義)
├── insert_data.sql         # 資料庫 DML (模擬真實情境的測試資料)
├── backend/                # FastAPI 後端目錄
│   ├── database.py         # DB 連線設定
│   ├── models.py           # SQLAlchemy ORM 模型
│   ├── schemas.py          # Pydantic 驗證格式
│   ├── main.py             # 核心 API 路由與邏輯
│   └── setup_db.py         # 一鍵初始化測試資料庫的腳本
└── frontend/               # 網頁前端目錄 (HTML/CSS/JS)
```

## 🚀 快速啟動指南

### 1. 啟動後端 API 伺服器
進入 `backend` 目錄並安裝所需套件：
```bash
cd backend
pip install -r requirements.txt
```
初始化本地測試資料庫 (SQLite)：
```bash
python setup_db.py
```
啟動 FastAPI 伺服器：
```bash
uvicorn main:app --reload
```
啟動後，請瀏覽 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** 即可進入 Swagger UI 測試 API。

### 2. 開啟前端介面
伺服器啟動後，使用瀏覽器直接開啟 `frontend/index.html` 檔案即可開始體驗玻璃擬態 (Glassmorphism) 風格的使用者介面。

## 👥 開發團隊
- 第 3 組 
- 指導教授：簡碩辰 教授
- 軟工二 411272004 李昕穎
- 軟工二 411377002 黃珈昱
- 軟工二 411377016 許云馨
- 工設四 411072026 許恆寧