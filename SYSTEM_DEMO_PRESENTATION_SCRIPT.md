# 系統展示講稿：資料庫邏輯加強版

## 展示前準備

打開：

- 前端：http://127.0.0.1:5500/index.html
- 後端文件：http://127.0.0.1:8000/docs

測試帳號：

- `winnie@example.com`
- `hashed_pw_1`

展示前先檢查兩件事：

- 前端右上角語言切換為中文時，按鈕應顯示「搜尋、購買、詳細資料、評價賣家、發布、登出」。
- 若要展示 `Mingyu and Wonwoo card set` 的搜尋與 Wishlist 撮合，該商品狀態必須是 `Available`。如果搜尋 `Mingyu` 沒有結果，代表它可能已被訂單買走，狀態變成 `Sold`。

目前系統核心資料表：

- `User`
- `Group`
- `Member`
- `Product`
- `Product_Member_Rel`
- `Order`
- `Wishlist`
- `Review`

目前我檢查到的資料庫實際資料量：

- `User`: 4 筆
- `Group`: 6 筆
- `Member`: 15 筆
- `Product`: 5 筆
- `Product_Member_Rel`: 6 筆
- `Order`: 2 筆
- `Wishlist`: 2 筆
- `Review`: 2 筆

如果你要照原本「一筆訂單、一筆評價」版本展示，展示前要先把多出來的測試訂單與評價清掉，讓畫面回到最乾淨的展示資料。

## 1. 開場

你可以說：

我們的系統是「偶像周邊二手交易與訂單管理系統」。它不是單純的買賣網站，而是把偶像周邊交易中的商品、成員、願望清單、訂單、評價全部轉成關聯式資料庫管理。

接著補一句資料庫重點：

目前系統有 8 張核心資料表：`User`、`Group`、`Member`、`Product`、`Product_Member_Rel`、`Order`、`Wishlist`、`Review`。

這一頁最後補充：

這個系統背後對應的是完整的關聯式資料庫設計，核心關係包含會員與訂單、商品與成員、願望清單與成員、訂單與評價；SQL 概念包含主鍵、外鍵、一對多、多對多與聚合查詢。

## 2. 展示商品搜尋

操作：

1. 登入系統。
2. 在首頁成員搜尋輸入 `Mingyu`。
3. 按「搜尋」。

預期系統會找到：

- 商品：`Mingyu and Wonwoo card set`
- 團體：`SEVENTEEN`
- 成員：`Mingyu, Wonwoo`
- 價格：`NT$500`
- 狀況：`Used - Good`
- 交易方式：`Shipping`

你要說：

這裡不是單純用商品名稱搜尋，而是透過 `Product`、`Product_Member_Rel`、`Member`、`Group` 做 JOIN。因為這個商品同時標記 Mingyu 和 Wonwoo，所以搜尋 Mingyu 也能找到雙人卡。

這是第一個資料庫亮點：N:M 多對多關係。

這一頁最後補充：

這個功能背後對應的是 `Product`、`Member`、`Group` 和中介表 `Product_Member_Rel`；商品與成員是多對多關係；SQL 概念是 `JOIN`、`WHERE` 條件查詢，以及透過中介表完成多成員商品搜尋。

## 3. 展示 Wishlist 撮合

操作：

1. 點「願望清單」。
2. 看「媒合商品」區塊。

預期系統會撮合到：

- Wishlist 目標成員：`Mingyu`
- 符合商品：`Mingyu and Wonwoo card set`
- 商品價格：`NT$500`
- 買家預算：`NT$600`

你要說：

`Wishlist` 表記錄使用者想找的成員與最高價格。系統會自動比對 `Available` 商品、商品價格和 `Product_Member_Rel` 成員關聯，找出符合條件的商品。這就是企畫書中提到的「貨找人」。

這是第二個資料庫亮點：Wishlist matching / 自動撮合查詢。

這一頁最後補充：

這個功能背後對應的是 `Wishlist`、`Product`、`Product_Member_Rel` 和 `Member`；關係上是使用者對願望清單的一對多，以及商品對成員的多對多；SQL 概念是 `JOIN`、條件比對、`Price <= MaxPrice`，以及 `Status = 'Available'` 的篩選。

## 4. 展示訂單狀態

操作：

1. 點「訂單」。
2. 展示目前訂單卡片。

如果使用乾淨展示資料，主要訂單資料為：

- `OrderID`: 1
- `BuyerID`: 1
- `ProductID`: 3
- `OrderPrice`: `NT$800`
- `Status`: `Completed`

你要說：

`Order` 表會保留 `OrderPrice`，也就是下單當下的價格快照。即使商品未來改價，歷史訂單金額也不會被影響。

再補狀態機：

新訂單會從 `Pending` 開始，接著可以更新為 `Shipped`，最後才是 `Completed`。這對應企畫書中的訂單狀態控管。

這是第三個資料庫亮點：歷史快照 + 訂單狀態機。

這一頁最後補充：

這個功能背後對應的是 `Order`、`User` 和 `Product`；買家與訂單是一對多關係，商品與訂單用 `ProductID` 連結；SQL 概念是 `INSERT` 建立訂單、`UPDATE` 更新狀態、`WHERE` 查詢特定使用者訂單，以及用 `OrderPrice` 保存歷史價格快照。

## 5. 展示評價與信譽

操作：

1. 在 `Completed` 訂單後點「評價賣家」。
2. 展示評分欄位。

你要說：

我們的評價不是一般星等，而是針對偶像周邊交易設計三個指標：包裝分數、對光或影片確認分數、出貨速度分數。

如果使用乾淨展示資料，目前賣家信譽排行資料為：

- 賣家：`kpop_lover`
- `ReviewCount`: 1
- 包裝平均：5.0
- 影片平均：4.0
- 速度平均：5.0
- 總信譽：4.67

你要說：

系統會用 `Review` 表的三個分數做 `AVG` 聚合，重新計算賣家信譽，並回寫到 `User` 表。

這是第四個資料庫亮點：AVG 聚合 + 信譽回寫。

這一頁最後補充：

這個功能背後對應的是 `Review`、`Order`、`Product` 和 `User`；一筆訂單對應一筆評價，評價再透過訂單商品找到賣家；SQL 概念是 `AVG` 聚合、`GROUP BY` 賣家分組，以及把計算結果更新回 `User.SellerReputation`。

## 6. 展示 Analytics

操作：

1. 點「分析」。
2. 展示三個分析區塊。

### 6-1. 市場歷史均價

如果使用乾淨展示資料，市場歷史均價會有：

- `IVE Wonyoung`
- 交易數：1
- 平均價格：`NT$800`
- 最低：`NT$800`
- 最高：`NT$800`

你要說：

這裡使用 `Completed` 訂單計算市場歷史均價，使用 `GROUP BY`、`AVG`、`MIN`、`MAX`。這直接對應企畫書中提到的未來可分析市場均價。

這一頁最後補充：

這個功能背後對應的是 `Order`、`Product`、`Product_Member_Rel`、`Member` 和 `Group`；關係是訂單連到商品，商品再透過中介表連到成員與團體；SQL 概念是 `GROUP BY`、`AVG`、`MIN`、`MAX`，只統計 `Completed` 的歷史成交資料。

### 6-2. 成員需求熱度

如果使用乾淨展示資料，成員需求熱度會有：

- `SEVENTEEN Mingyu`
- `WishlistCount`: 1
- 平均預算：`NT$600`
- 可撮合商品數：1

- `NewJeans Haerin`
- `WishlistCount`: 1
- 平均預算：`NT$400`
- 可撮合商品數：1

你要說：

這裡用 `Wishlist` 做 `COUNT` 和 `AVG`，可以知道哪些成員需求高、平均預算是多少，也能看目前有多少商品能撮合。

這一頁最後補充：

這個功能背後對應的是 `Wishlist`、`Member`、`Group`、`Product` 和 `Product_Member_Rel`；關係是願望清單指定成員，商品透過多對多關係標記成員；SQL 概念是 `COUNT`、`AVG`、`GROUP BY`，以及條件式撮合查詢。

### 6-3. 賣家信譽排行

如果使用乾淨展示資料，賣家信譽排行會有：

- `kpop_lover`
- 評價數：1
- 總信譽：4.67

你要說：

這個區塊展示 `Review` 資料如何被聚合成賣家排行，讓資料庫不只是儲存資料，也能產生決策資訊。

這一頁最後補充：

這個功能背後對應的是 `Review`、`Order`、`Product` 和 `User`；關係是評價連到訂單、訂單連到商品、商品連到賣家；SQL 概念是 `JOIN`、`GROUP BY`、`AVG`、`COUNT`，用來產生賣家排行。

## 7. 後端文件對應

操作：

1. 打開 http://127.0.0.1:8000/docs
2. 指出每個 API 都有對應的資料庫表與前端功能。

你要說：

這一頁可以看到系統不是只有畫面，而是每個功能都可以對應到後端 API。像商品搜尋對應 `/products/search`，Wishlist 撮合對應 `/users/{user_id}/wishlist_matches`，訂單對應 `/orders/` 和 `/orders/{order_id}/status`，分析對應 `/analytics/...`。

這一頁最後補充：

這個頁面背後展示的是前端、API 與資料庫的三層對應；資料庫表負責儲存與關聯，API 負責把 SQL 查詢包裝成系統功能，前端則把查詢結果轉成使用者可以操作的畫面。

## 8. 資料庫總結

最後你可以這樣收尾：

我們系統的特色是把偶像周邊交易中最難管理的幾件事，包含多成員商品搜尋、願望清單撮合、訂單狀態追蹤、領域化評價與市場均價分析，都轉換成可查詢、可追蹤、可分析的關聯式資料庫設計。

正式展示最重要的一句話：

每展示一頁，我都會補上這個功能背後對應的是哪張表、哪個關係、哪個 SQL 概念。

快速對照：

- 商品搜尋：`Product_Member_Rel`、多對多、`JOIN`
- Wishlist：`Wishlist`、條件比對、`JOIN`
- 訂單：`Order`、狀態機、歷史快照、`INSERT` / `UPDATE`
- 評價：`Review`、`AVG`、信譽回寫
- Analytics：`GROUP BY`、`AVG`、`COUNT`、`MIN`、`MAX`
