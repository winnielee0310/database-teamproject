-- 建立資料庫表格 (DDL)

-- 1. 使用者 (User)
CREATE TABLE `User` (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Account VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    SellerReputation DECIMAL(3, 2) DEFAULT 5.00,
    BuyerReputation DECIMAL(3, 2) DEFAULT 5.00
);

-- 2. 團體 (Group)
CREATE TABLE `Group` (
    GroupID INTEGER PRIMARY KEY AUTOINCREMENT,
    GroupName VARCHAR(100) NOT NULL,
    Company VARCHAR(100)
);

-- 3. 成員 (Member)
CREATE TABLE `Member` (
    MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
    GroupID INTEGER NOT NULL,
    MemberName VARCHAR(100) NOT NULL,
    FOREIGN KEY (GroupID) REFERENCES `Group`(GroupID) ON DELETE CASCADE
);

-- 4. 商品 (Product)
CREATE TABLE `Product` (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    SellerID INTEGER NOT NULL,
    Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0),
    Condition VARCHAR(50) NOT NULL, -- 例如：全新、近全新、微損
    TradeMethod VARCHAR(50) NOT NULL, -- 例如：面交、郵寄、超商取貨
    Status VARCHAR(20) DEFAULT 'Available', -- Available, Sold, Removed
    FOREIGN KEY (SellerID) REFERENCES `User`(UserID)
);

-- 5. 商品成員關聯 (Product_Member_Rel)
CREATE TABLE `Product_Member_Rel` (
    RelID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER NOT NULL,
    MemberID INTEGER NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES `Product`(ProductID) ON DELETE CASCADE,
    FOREIGN KEY (MemberID) REFERENCES `Member`(MemberID) ON DELETE CASCADE
);

-- 6. 訂單 (Order)
CREATE TABLE `Order` (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    BuyerID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL UNIQUE, -- 1:1 對應商品
    OrderPrice DECIMAL(10, 2) NOT NULL CHECK (OrderPrice >= 0),
    Status VARCHAR(20) DEFAULT 'Pending', -- Pending, Shipped, Completed
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (BuyerID) REFERENCES `User`(UserID),
    FOREIGN KEY (ProductID) REFERENCES `Product`(ProductID)
);

-- 7. 願望清單 (Wishlist)
CREATE TABLE `Wishlist` (
    WishID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    MemberID INTEGER NOT NULL,
    MaxPrice DECIMAL(10, 2) NOT NULL CHECK (MaxPrice >= 0),
    ConditionReq VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES `User`(UserID) ON DELETE CASCADE,
    FOREIGN KEY (MemberID) REFERENCES `Member`(MemberID) ON DELETE CASCADE
);

-- 8. 評價 (Review)
CREATE TABLE `Review` (
    ReviewID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER NOT NULL UNIQUE, -- 1:1 對應訂單
    PackingScore INTEGER NOT NULL CHECK (PackingScore BETWEEN 1 AND 5),
    VideoScore INTEGER NOT NULL CHECK (VideoScore BETWEEN 1 AND 5),
    SpeedScore INTEGER NOT NULL CHECK (SpeedScore BETWEEN 1 AND 5),
    Comment TEXT,
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID) ON DELETE CASCADE
);
