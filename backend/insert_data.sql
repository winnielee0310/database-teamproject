INSERT INTO `User` (`帳號`, `密碼`, `電子郵件`, `賣家評價`, `買家評價`) VALUES
('winnie_01', 'hashed_pw_1', 'winnie@example.com', 4.8, 4.9),
('fan_boy_99', 'hashed_pw_2', 'fanboy@example.com', 5.0, 4.5),
('kpop_lover', 'hashed_pw_3', 'lover@example.com', 4.2, 5.0),
('demo_user', 'demo1234', 'demo@example.com', 5.0, 5.0);

INSERT INTO `Group` (`團體名稱`, `公司`) VALUES
('NewJeans', 'ADOR'),
('SEVENTEEN', 'PLEDIS'),
('IVE', 'Starship'),
('BLACKPINK', 'YG Entertainment'),
('aespa', 'SM Entertainment'),
('BTS', 'BIGHIT MUSIC');

INSERT INTO `Member` (`團體編號`, `成員名稱`) VALUES
(1, 'Minji'), (1, 'Hanni'), (1, 'Danielle'), (1, 'Haerin'), (1, 'Hyein'),
(2, 'Jeonghan'), (2, 'Mingyu'), (2, 'Wonwoo'),
(3, 'Wonyoung'), (3, 'Yujin'), (3, 'Liz'),
(4, 'Jisoo'), (4, 'Rose'),
(5, 'Karina'),
(6, 'Jungkook');

INSERT INTO `Product` (`賣家編號`, `價格`, `商品名稱`, `商品描述`, `商品狀況`, `交易方式`, `狀態`, `圖片網址`) VALUES
(1, 350.00, 'Haerin photocard', 'NewJeans Haerin official photocard in sleeve.', 'New', 'Meetup', 'Available', NULL),
(2, 500.00, 'Mingyu and Wonwoo card set', 'SEVENTEEN card set, good corners and clean surface.', 'Used - Good', 'Shipping', 'Available', NULL),
(3, 800.00, 'Wonyoung album inclusions', 'IVE Wonyoung album inclusions bundle.', 'Like New', 'Mailing', 'Sold', NULL),
(4, 280.00, 'Karina mini photocard', 'aespa Karina mini photocard.', 'New', 'Meetup', 'Available', 'demo_products/aespa_karina_card.jpg'),
(4, 2500.00, 'BTS ARMY BOMB light stick', 'Official light stick with box.', 'Used - Good', 'Shipping', 'Available', 'demo_products/bts_jungkook_lightstick.jpg');

INSERT INTO `Product_Member_Rel` (`商品編號`, `成員編號`) VALUES
(1, 4),
(2, 7), (2, 8),
(3, 9),
(4, 14),
(5, 15);

INSERT INTO `Wishlist` (`使用者編號`, `成員編號`, `最高價格`, `狀況需求`) VALUES
(2, 4, 400.00, 'New'),
(1, 7, 600.00, 'Any');

INSERT INTO `Order` (`買家編號`, `商品編號`, `訂單金額`, `狀態`) VALUES
(1, 3, 800.00, 'Completed');

INSERT INTO `Review` (`訂單編號`, `包裝分數`, `影片分數`, `速度分數`, `評論`) VALUES
(1, 5, 4, 5, 'Packed safely and shipped quickly.');
