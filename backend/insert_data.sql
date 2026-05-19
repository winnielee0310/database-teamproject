-- 插入測試資料 (DML)

-- 1. 插入使用者
INSERT INTO `User` (Account, Password, Email, SellerReputation, BuyerReputation) VALUES 
('winnie_01', 'hashed_pw_1', 'winnie@example.com', 4.8, 4.9),
('fan_boy_99', 'hashed_pw_2', 'fanboy@example.com', 5.0, 4.5),
('kpop_lover', 'hashed_pw_3', 'lover@example.com', 4.2, 5.0);

-- 2. 插入團體
INSERT INTO `Group` (GroupName, Company) VALUES 
('NewJeans', 'ADOR'),
('SEVENTEEN', 'PLEDIS'),
('IVE', 'Starship');

-- 3. 插入成員
INSERT INTO `Member` (GroupID, MemberName) VALUES 
(1, 'Minji'), (1, 'Hanni'), (1, 'Danielle'), (1, 'Haerin'), (1, 'Hyein'),
(2, 'Jeonghan'), (2, 'Mingyu'), (2, 'Wonwoo'),
(3, 'Wonyoung'), (3, 'Yujin');

-- 4. 插入商品 (包含單人卡與雙人卡)
INSERT INTO `Product` (SellerID, Price, Condition, TradeMethod, Status) VALUES 
(1, 350.00, '全新', '面交', 'Available'),   -- Haerin 小卡
(2, 500.00, '近全新', '超商取貨', 'Available'), -- Mingyu & Wonwoo 雙人卡
(3, 800.00, '微損', '郵寄', 'Sold');          -- Wonyoung 專輯

-- 5. 插入商品成員關聯
-- 商品 1 是 Haerin 單人卡
INSERT INTO `Product_Member_Rel` (ProductID, MemberID) VALUES (1, 4);
-- 商品 2 是 Mingyu & Wonwoo 雙人卡 (解決 N:M 關聯)
INSERT INTO `Product_Member_Rel` (ProductID, MemberID) VALUES (2, 7), (2, 8);
-- 商品 3 是 Wonyoung
INSERT INTO `Product_Member_Rel` (ProductID, MemberID) VALUES (3, 9);

-- 6. 插入願望清單
INSERT INTO `Wishlist` (UserID, MemberID, MaxPrice, ConditionReq) VALUES 
(2, 4, 400.00, '全新'), -- 尋找 Haerin 全新小卡，預算 400
(1, 7, 600.00, '不限'); -- 尋找 Mingyu 相關周邊，預算 600

-- 7. 插入訂單 (商品 3 已售出)
INSERT INTO `Order` (BuyerID, ProductID, OrderPrice, Status) VALUES 
(1, 3, 800.00, 'Completed');

-- 8. 插入評價 (針對訂單 1)
INSERT INTO `Review` (OrderID, PackingScore, VideoScore, SpeedScore, Comment) VALUES 
(1, 5, 4, 5, '包裝很完美，出貨也很快！');
