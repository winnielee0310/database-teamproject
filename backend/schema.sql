PRAGMA foreign_keys = ON;

CREATE TABLE `User` (
    `使用者編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `帳號` VARCHAR(50) NOT NULL UNIQUE,
    `密碼` VARCHAR(255) NOT NULL,
    `電子郵件` VARCHAR(100) NOT NULL UNIQUE,
    `賣家評價` DECIMAL(3, 2) DEFAULT 5.00,
    `買家評價` DECIMAL(3, 2) DEFAULT 5.00
);

CREATE TABLE `Group` (
    `團體編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `團體名稱` VARCHAR(100) NOT NULL,
    `公司` VARCHAR(100)
);

CREATE TABLE `Member` (
    `成員編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `團體編號` INTEGER NOT NULL,
    `成員名稱` VARCHAR(100) NOT NULL,
    FOREIGN KEY (`團體編號`) REFERENCES `Group`(`團體編號`) ON DELETE CASCADE
);

CREATE TABLE `Product` (
    `商品編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `賣家編號` INTEGER NOT NULL,
    `價格` DECIMAL(10, 2) NOT NULL CHECK (`價格` >= 0),
    `商品名稱` VARCHAR(100) NOT NULL,
    `商品描述` TEXT,
    `商品狀況` VARCHAR(50) NOT NULL,
    `交易方式` VARCHAR(50) NOT NULL,
    `狀態` VARCHAR(20) DEFAULT 'Available',
    `圖片網址` VARCHAR(255),
    FOREIGN KEY (`賣家編號`) REFERENCES `User`(`使用者編號`)
);

CREATE TABLE `Product_Member_Rel` (
    `關聯編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `商品編號` INTEGER NOT NULL,
    `成員編號` INTEGER NOT NULL,
    FOREIGN KEY (`商品編號`) REFERENCES `Product`(`商品編號`) ON DELETE CASCADE,
    FOREIGN KEY (`成員編號`) REFERENCES `Member`(`成員編號`) ON DELETE CASCADE
);

CREATE TABLE `Order` (
    `訂單編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `買家編號` INTEGER NOT NULL,
    `商品編號` INTEGER NOT NULL UNIQUE,
    `訂單金額` DECIMAL(10, 2) NOT NULL CHECK (`訂單金額` >= 0),
    `狀態` VARCHAR(20) DEFAULT 'Pending',
    `訂單日期` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`買家編號`) REFERENCES `User`(`使用者編號`),
    FOREIGN KEY (`商品編號`) REFERENCES `Product`(`商品編號`)
);

CREATE TABLE `Wishlist` (
    `願望編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `使用者編號` INTEGER NOT NULL,
    `成員編號` INTEGER NOT NULL,
    `最高價格` DECIMAL(10, 2) NOT NULL CHECK (`最高價格` >= 0),
    `狀況需求` VARCHAR(50),
    FOREIGN KEY (`使用者編號`) REFERENCES `User`(`使用者編號`) ON DELETE CASCADE,
    FOREIGN KEY (`成員編號`) REFERENCES `Member`(`成員編號`) ON DELETE CASCADE
);

CREATE TABLE `Review` (
    `評價編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `訂單編號` INTEGER NOT NULL UNIQUE,
    `包裝分數` INTEGER NOT NULL CHECK (`包裝分數` BETWEEN 1 AND 5),
    `影片分數` INTEGER NOT NULL CHECK (`影片分數` BETWEEN 1 AND 5),
    `速度分數` INTEGER NOT NULL CHECK (`速度分數` BETWEEN 1 AND 5),
    `評論` TEXT,
    FOREIGN KEY (`訂單編號`) REFERENCES `Order`(`訂單編號`) ON DELETE CASCADE
);

CREATE TABLE `ProductMessage` (
    `訊息編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `商品編號` INTEGER NOT NULL,
    `發送者編號` INTEGER NOT NULL,
    `接收者編號` INTEGER NOT NULL,
    `內容` TEXT NOT NULL,
    `媒體網址` VARCHAR(255),
    `發送時間` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`商品編號`) REFERENCES `Product`(`商品編號`) ON DELETE CASCADE,
    FOREIGN KEY (`發送者編號`) REFERENCES `User`(`使用者編號`),
    FOREIGN KEY (`接收者編號`) REFERENCES `User`(`使用者編號`)
);

CREATE TABLE `Chat` (
    `聊天室編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `商品編號` INTEGER NOT NULL,
    `買家編號` INTEGER NOT NULL,
    `賣家編號` INTEGER NOT NULL,
    `建立時間` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`商品編號`) REFERENCES `Product`(`商品編號`) ON DELETE CASCADE,
    FOREIGN KEY (`買家編號`) REFERENCES `User`(`使用者編號`),
    FOREIGN KEY (`賣家編號`) REFERENCES `User`(`使用者編號`)
);

CREATE TABLE `ChatMessage` (
    `訊息編號` INTEGER PRIMARY KEY AUTOINCREMENT,
    `聊天室編號` INTEGER NOT NULL,
    `發送者編號` INTEGER NOT NULL,
    `訊息內容` TEXT NOT NULL,
    `是否已讀` BOOLEAN DEFAULT 0,
    `建立時間` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`聊天室編號`) REFERENCES `Chat`(`聊天室編號`) ON DELETE CASCADE,
    FOREIGN KEY (`發送者編號`) REFERENCES `User`(`使用者編號`)
);

CREATE INDEX IF NOT EXISTS `idx_member_group_id` ON `Member` (`團體編號`);
CREATE INDEX IF NOT EXISTS `idx_member_name` ON `Member` (`成員名稱`);
CREATE INDEX IF NOT EXISTS `idx_group_name` ON `Group` (`團體名稱`);
CREATE INDEX IF NOT EXISTS `idx_product_seller_id` ON `Product` (`賣家編號`);
CREATE INDEX IF NOT EXISTS `idx_product_status` ON `Product` (`狀態`);
CREATE INDEX IF NOT EXISTS `idx_product_price` ON `Product` (`價格`);
CREATE INDEX IF NOT EXISTS `idx_product_member_product` ON `Product_Member_Rel` (`商品編號`);
CREATE INDEX IF NOT EXISTS `idx_product_member_member` ON `Product_Member_Rel` (`成員編號`);
CREATE INDEX IF NOT EXISTS `idx_order_buyer` ON `Order` (`買家編號`);
CREATE INDEX IF NOT EXISTS `idx_wishlist_user` ON `Wishlist` (`使用者編號`);
CREATE INDEX IF NOT EXISTS `idx_wishlist_member` ON `Wishlist` (`成員編號`);
CREATE INDEX IF NOT EXISTS `idx_chat_participants` ON `Chat` (`買家編號`, `賣家編號`);
CREATE INDEX IF NOT EXISTS `idx_chat_message_chat` ON `ChatMessage` (`聊天室編號`);
