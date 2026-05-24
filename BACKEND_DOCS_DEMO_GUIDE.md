# 後端文件 `/docs` 展示教學

後端文件網址：

```text
http://127.0.0.1:8000/docs
```

這個頁面是 FastAPI 自動產生的 Swagger UI。  
報告時可以用它展示每個前端功能背後對應的 API、資料表與資料庫概念。

---

## 一、怎麼看 `/docs`

每一列 API 會有三個重點：

```text
HTTP 方法 + API 路徑 + 功能名稱
```

例如：

```text
GET /products/search
```

代表這是一個查詢商品的 API。

常見 HTTP 方法：

| 方法 | 意義 | 報告時可怎麼說 |
|---|---|---|
| GET | 查詢資料 | 從資料庫讀取資料 |
| POST | 新增資料 | 將資料寫入資料庫 |
| PATCH | 局部更新資料 | 更新某筆資料的狀態 |

---

## 二、Swagger UI 操作方式

1. 打開 `http://127.0.0.1:8000/docs`
2. 找到要展示的 API 分組，例如 `Products`
3. 點開 API，例如 `GET /products/search`
4. 按右上角 `Try it out`
5. 輸入參數或 Request body
6. 按 `Execute`
7. 看下方：
   - Request URL：實際送出的網址
   - Response body：後端從資料庫查到的結果
   - Response code：成功通常是 200

---

## 三、報告展示順序與 API 對應

### 1. Auth：登入

API：

```text
POST /auth/login
```

Request body：

```json
{
  "email": "winnie@example.com",
  "password": "hashed_pw_1"
}
```

用途：

- 對應前端登入畫面
- 查詢 `User` 表

展示說法：

> 登入時後端會到 User 表確認 Email 與 Password，成功後回傳使用者編號與帳號。

---

### 2. Idols：團體與成員

API：

```text
GET /groups/
GET /members/
GET /groups/{group_id}/members
```

用途：

- 對應團體與成員資料
- 對應 `Group` 與 `Member` 表

展示說法：

> 團體和成員沒有直接寫死在商品文字中，而是獨立成 Group 與 Member 表，方便後續搜尋與關聯。

---

### 3. Products：商品搜尋

API：

```text
GET /products/search
```

Try it out 參數：

```text
member_name = Mingyu
```

實際結果：

```text
Mingyu and Wonwoo card set
MemberNames: Mingyu, Wonwoo
GroupNames: SEVENTEEN
Price: 500
```

對應資料表：

- `Product`
- `Product_Member_Rel`
- `Member`
- `Group`

展示說法：

> 這個搜尋不是單純比對商品名稱，而是透過 Product_Member_Rel 連接 Product 與 Member，所以可以解決雙人卡或小分隊卡搜尋問題。

資料庫概念：

- 多對多關係
- 中介表
- JOIN 查詢

---

### 4. Wishlist：願望清單撮合

API：

```text
GET /users/{user_id}/wishlist_matches
```

Try it out 參數：

```text
user_id = 1
```

實際結果：

```text
WishID: 2
MemberName: Mingyu
ProductName: Mingyu and Wonwoo card set
Price: 500
```

對應資料表：

- `Wishlist`
- `Product`
- `Product_Member_Rel`
- `Member`

展示說法：

> Wishlist 表記錄使用者想找的成員與最高預算，系統會自動比對 Available 商品，這就是企畫書中的「貨找人」。

資料庫概念：

- 條件查詢
- JOIN
- 預算比對

---

### 5. Orders：訂單查詢與狀態更新

查詢訂單 API：

```text
GET /users/{user_id}/orders
```

Try it out 參數：

```text
user_id = 1
```

更新訂單 API：

```text
PATCH /orders/{order_id}/status
```

Try it out 參數：

```text
order_id = 1
```

Request body：

```json
{
  "Status": "Completed"
}
```

對應資料表：

- `Order`
- `Product`

展示說法：

> 訂單狀態流程是 Pending -> Shipped -> Completed。Order 表也保留 OrderPrice，確保歷史交易價格不會因商品改價而改變。

資料庫概念：

- 狀態機
- 歷史快照
- 更新資料

---

### 6. Users：賣家信譽

API：

```text
GET /users/{user_id}/reputation
```

Try it out 參數：

```text
user_id = 3
```

實際結果：

```text
Average_Packing: 5.0
Average_Video: 4.0
Average_Speed: 5.0
Total_Reputation: 4.67
```

對應資料表：

- `User`
- `Product`
- `Order`
- `Review`

展示說法：

> Review 表保存包裝、影片、速度三項分數，後端會用 AVG 計算賣家信譽並回寫到 User 表。

資料庫概念：

- AVG 聚合
- 多表 JOIN
- 彙總欄位回寫

---

### 7. Analytics：資料庫分析亮點

API：

```text
GET /analytics/market_average
GET /analytics/member_demand
GET /analytics/seller_ranking
```

對應前端：

```text
Analytics 頁籤
```

展示說法：

> Analytics 是本系統的資料庫亮點，展示系統不只是 CRUD，而是能透過 SQL 聚合查詢產生分析結果。

三個分析：

| API | 功能 | SQL 概念 |
|---|---|---|
| `/analytics/market_average` | 市場歷史均價 | GROUP BY, AVG, MIN, MAX |
| `/analytics/member_demand` | 成員需求熱度 | COUNT, AVG, GROUP BY |
| `/analytics/seller_ranking` | 賣家信譽排行 | AVG, JOIN |

---

## 四、前端功能與後端 API 對照表

| 前端展示功能 | 後端 API | 對應資料表 | 資料庫重點 |
|---|---|---|---|
| 登入 | `POST /auth/login` | User | 條件查詢 |
| 團體/成員資料 | `GET /groups/`, `GET /members/` | Group, Member | 1:N |
| 商品搜尋 | `GET /products/search` | Product, Product_Member_Rel, Member, Group | N:M, JOIN |
| 商品上架 | `POST /products/` | Product, Product_Member_Rel | 新增資料, 多對多 |
| 願望清單 | `POST /wishlists/` | Wishlist | 新增需求 |
| Wishlist 撮合 | `GET /users/{id}/wishlist_matches` | Wishlist, Product, Product_Member_Rel | JOIN, 條件比對 |
| 訂單查詢 | `GET /users/{id}/orders` | Order | 查詢交易 |
| 訂單狀態更新 | `PATCH /orders/{id}/status` | Order | 狀態機 |
| 評價賣家 | `POST /reviews/` | Review | 新增評價 |
| 信譽分數 | `GET /users/{id}/reputation` | Review, User | AVG, 回寫 |
| 市場分析 | `GET /analytics/*` | 多表 | GROUP BY, AVG, COUNT |

---

## 五、報告時最推薦展示的 API

如果時間有限，優先展示這五個：

1. `GET /products/search?member_name=Mingyu`
2. `GET /users/1/wishlist_matches`
3. `GET /users/1/orders`
4. `GET /users/3/reputation`
5. `GET /analytics/market_average`

這五個最能證明：

- 多對多關係
- Wishlist 撮合
- 訂單管理
- 評價聚合
- 資料庫分析

---

## 六、總結講法

> `/docs` 可以看到每個前端功能背後實際呼叫的 API。  
> 我們可以從 API 進一步對應到資料表與 SQL 概念，例如商品搜尋對應 Product_Member_Rel 的多對多 JOIN，Wishlist 對應條件撮合，Analytics 對應 GROUP BY 與 AVG 聚合查詢。這能證明本系統不是單純前端展示，而是完整的關聯式資料庫應用。
