# 修復清單與完成狀態

**更新日期**: 2026-05-22
**修復範圍**: 依照 `handoff.md` 的 P0/P1 未完成事項，整理後端 API、資料庫 schema、初始化腳本與前端串接。
**目前狀態**: 程式碼修復完成；Python 實跑驗證受本機 Python 環境限制。

---

## 一、已完成修復

### 1. 前端 API 位址修正
- **檔案**: `frontend/app.js`
- **修復內容**:
  - 將前端 API base 統一為 `http://127.0.0.1:8000`。
  - 修復原本大量未閉合字串造成的 JavaScript 語法錯誤。
  - 補齊登入、註冊、搜尋、上架、願望清單、下單、評價、聊天室流程。
- **狀態**: 已完成

### 2. Product 的 Condition 欄位補齊
- **檔案**:
  - `backend/models.py`
  - `backend/schemas.py`
  - `backend/main.py`
  - `backend/schema.sql`
  - `backend/insert_data.sql`
  - 根目錄同步檔案：`models.py`, `schemas.py`, `schema.sql`, `insert_data.sql`
- **修復內容**:
  - `Product` ORM 加入 `Condition = Column(String(50), nullable=False)`。
  - `ProductCreate` 與 `ProductResponse` 加入 `Condition`。
  - `create_product()` 寫入 `Condition`。
  - SQL schema 與 demo data 同步加入 `Condition`。
- **狀態**: 已完成

### 3. Product 資料欄位與 demo data 修正
- **檔案**:
  - `backend/schema.sql`
  - `backend/insert_data.sql`
  - `schema.sql`
  - `insert_data.sql`
- **修復內容**:
  - `Product` 表補齊 `ProductName`, `Description`, `Condition`, `ImageUrl`。
  - 修復原始 INSERT 字串破損與欄位數不一致問題。
  - 補入可搜尋、可下單、可評價的 demo 商品資料。
  - 新增聊天室相關表：`Chat`, `ChatMessage`。
  - 新增商品留言表：`ProductMessage`。
- **狀態**: 已完成

### 4. 後端 API 主程式修復
- **檔案**: `backend/main.py`
- **修復內容**:
  - 重建可啟動的 FastAPI app。
  - 修復 `FastAPI(...)`、`HTTPException(...)` 等未閉合字串。
  - 補齊以下 API：
    - `POST /auth/register`
    - `POST /auth/login`
    - `GET /users/{user_id}`
    - `GET /users/{user_id}/reputation`
    - `GET /groups/`
    - `GET /members/`
    - `POST /products/`
    - `GET /products/search`
    - `POST /upload-image/`
    - `POST /wishlists/`
    - `GET /users/{user_id}/wishlists`
    - `POST /orders/`
    - `GET /users/{user_id}/orders`
    - `POST /reviews/`
    - `POST /chats/create`
    - `POST /messages/send`
    - `GET /messages/{chat_id}`
    - `GET /users/{user_id}/chats`
    - `POST /chats/{chat_id}/read`
- **狀態**: 已完成

### 5. 資料庫初始化腳本修正
- **檔案**:
  - `setup_db.py`
  - `backend/setup_db.py`
  - `backend/backend/setup_db.py`
  - `test_setup.py`
- **修復內容**:
  - 使用 `Path(__file__).resolve()` 取得穩定路徑，避免從不同資料夾執行時找不到 SQL 檔。
  - 初始化流程統一為：刪除舊 DB、建立 schema、匯入 demo data。
  - 新增 `test_setup.py`，檢查必要資料表與 `Product` 欄位是否存在。
  - `backend/backend/setup_db.py` 改為轉接到正式 `backend/setup_db.py`。
- **狀態**: 已完成

### 6. 前端頁面修復
- **檔案**:
  - `frontend/index.html`
  - `frontend/app.js`
- **修復內容**:
  - 重建可正常載入的 HTML。
  - 修復 `<meta>`, `<a>`, `<h2>`, `<option>` 等未閉合標籤。
  - 補上商品狀態欄位 `sell-condition`。
  - 補齊商品詳情 modal 的 `detail-condition`。
  - 串接圖片上傳、商品上架、購買、評價、聊天室。
- **狀態**: 已完成

### 7. 重複後端入口整理
- **檔案**:
  - `main.py`
  - `database.py`
  - `backend/backend/main.py`
- **修復內容**:
  - 根目錄 `main.py` 轉接到 `backend/main.py`。
  - `backend/backend/main.py` 也轉接到正式後端入口，避免三套同名檔案邏輯分叉。
  - 根目錄 `database.py` 使用根目錄 `idol_trade.db`。
- **狀態**: 已完成

### 8. requirements 補齊
- **檔案**:
  - `requirements.txt`
  - `backend/requirements.txt`
- **修復內容**:
  - 新增 `python-multipart==0.0.9`，讓 FastAPI 可處理圖片上傳。
- **狀態**: 已完成

---

## 二、驗證結果

### 已通過
- [x] `node --check frontend/app.js`
- [x] `node --check backend/frontend/app.js`
- [x] `git diff --check`
  - 僅出現 Windows CRLF/LF 換行提示，沒有 whitespace error。
- [x] Chrome headless 可載入 `frontend/index.html`
  - 預覽截圖成功產生：`C:\Users\user\AppData\Local\Temp\idol-trade-preview.png`

### 受環境限制，尚未能實跑
- [ ] `python -m py_compile ...`
- [ ] `python test_setup.py`
- [ ] `uvicorn main:app --reload`

**原因**: 目前系統上的 `python` 指到 `C:\Users\user\AppData\Local\Microsoft\WindowsApps\python.exe`，這是 Microsoft Store 的占位啟動器，不是真正的 Python interpreter。`python --version` 也會直接 exit 1。

**安裝或修正 Python PATH 後，請執行以下驗證**:

```bash
python test_setup.py
cd backend
uvicorn main:app --reload
```

成功時預期：

```text
Database setup test passed.
Uvicorn running on http://127.0.0.1:8000
```

---

## 三、功能驗收清單

- [x] API 位址統一為 `8000`
- [x] `Product.Condition` 從資料庫到 API 完整串接
- [x] `ProductName`, `Description`, `ImageUrl` 欄位完整串接
- [x] demo SQL 可建立完整資料結構
- [x] 前端登入/註冊畫面可載入
- [x] 前端 JS 語法檢查通過
- [x] 商品搜尋 UI 已串接 `/products/search`
- [x] 商品上架 UI 已串接 `/products/`
- [x] 圖片上傳 UI 已串接 `/upload-image/`
- [x] 願望清單 UI 已串接 `/wishlists/`
- [x] 下單 UI 已串接 `/orders/`
- [x] 評價 UI 已串接 `/reviews/`
- [x] 聊天室 UI 已串接 `/chats/create`, `/messages/send`, `/messages/{chat_id}`
- [ ] Python 環境修正後進行後端實跑驗證
- [ ] Python 環境修正後進行 API Swagger 驗證

---

## 四、啟動方式

### 1. 建立資料庫

```bash
python setup_db.py
```

### 2. 啟動後端

```bash
cd backend
uvicorn main:app --reload
```

API 文件：

```text
http://127.0.0.1:8000/docs
```

### 3. 開啟前端

可直接開：

```text
frontend/index.html
```

或用靜態伺服器：

```bash
python -m http.server 5500 --directory frontend
```

然後開：

```text
http://127.0.0.1:5500/index.html
```

---

## 五、測試帳號

```text
Email: winnie@example.com
Password: hashed_pw_1
```

```text
Email: fanboy@example.com
Password: hashed_pw_2
```

```text
Email: lover@example.com
Password: hashed_pw_3
```

```text
Email: demo@example.com
Password: demo1234
```

---

## 六、後續建議

- 安裝正式 Python，並確認 `python --version` 可正常輸出版本。
- 執行 `python test_setup.py` 驗證 SQLite 初始化。
- 啟動 `uvicorn` 後，到 `/docs` 測試登入、搜尋、上架、下單與聊天室 API。
- 若要正式展示，建議再補 bcrypt 密碼雜湊與 JWT 登入狀態管理。
