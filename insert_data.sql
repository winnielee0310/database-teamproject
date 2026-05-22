INSERT INTO `User` (Account, Password, Email, SellerReputation, BuyerReputation) VALUES
('winnie_01', 'hashed_pw_1', 'winnie@example.com', 4.8, 4.9),
('fan_boy_99', 'hashed_pw_2', 'fanboy@example.com', 5.0, 4.5),
('kpop_lover', 'hashed_pw_3', 'lover@example.com', 4.2, 5.0),
('demo_user', 'demo1234', 'demo@example.com', 5.0, 5.0);

INSERT INTO `Group` (GroupName, Company) VALUES
('NewJeans', 'ADOR'),
('SEVENTEEN', 'PLEDIS'),
('IVE', 'Starship'),
('BLACKPINK', 'YG Entertainment'),
('aespa', 'SM Entertainment'),
('BTS', 'BIGHIT MUSIC');

INSERT INTO `Member` (GroupID, MemberName) VALUES
(1, 'Minji'), (1, 'Hanni'), (1, 'Danielle'), (1, 'Haerin'), (1, 'Hyein'),
(2, 'Jeonghan'), (2, 'Mingyu'), (2, 'Wonwoo'),
(3, 'Wonyoung'), (3, 'Yujin'), (3, 'Liz'),
(4, 'Jisoo'), (4, 'Rose'),
(5, 'Karina'),
(6, 'Jungkook');

INSERT INTO `Product` (SellerID, Price, ProductName, Description, Condition, TradeMethod, Status, ImageUrl) VALUES
(1, 350.00, 'Haerin photocard', 'NewJeans Haerin official photocard in sleeve.', 'New', 'Meetup', 'Available', NULL),
(2, 500.00, 'Mingyu and Wonwoo card set', 'SEVENTEEN card set, good corners and clean surface.', 'Used - Good', 'Shipping', 'Available', NULL),
(3, 800.00, 'Wonyoung album inclusions', 'IVE Wonyoung album inclusions bundle.', 'Like New', 'Mailing', 'Sold', NULL),
(4, 280.00, 'Karina mini photocard', 'aespa Karina mini photocard.', 'New', 'Meetup', 'Available', 'demo_products/aespa_karina_card.jpg'),
(4, 2500.00, 'BTS ARMY BOMB light stick', 'Official light stick with box.', 'Used - Good', 'Shipping', 'Available', 'demo_products/bts_jungkook_lightstick.jpg');

INSERT INTO `Product_Member_Rel` (ProductID, MemberID) VALUES
(1, 4),
(2, 7), (2, 8),
(3, 9),
(4, 14),
(5, 15);

INSERT INTO `Wishlist` (UserID, MemberID, MaxPrice, ConditionReq) VALUES
(2, 4, 400.00, 'New'),
(1, 7, 600.00, 'Any');

INSERT INTO `Order` (BuyerID, ProductID, OrderPrice, Status) VALUES
(1, 3, 800.00, 'Completed');

INSERT INTO `Review` (OrderID, PackingScore, VideoScore, SpeedScore, Comment) VALUES
(1, 5, 4, 5, 'Packed safely and shipped quickly.');
