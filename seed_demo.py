"""
seed_demo.py - 預設示意商品資料初始化

系統第一次啟動時，若 Product 表為空，自動建立 9 筆 KPOP 示意商品。
避免重複建立：若已有商品則跳過。
"""

from database import SessionLocal
import models


def seed_demo_products():
    """若 Product 資料表為空，自動插入 9 筆示意商品。"""
    db = SessionLocal()
    try:
        # 若已有商品，直接跳過
        existing = db.query(models.Product).count()
        if existing > 0:
            print(f"[seed_demo] 已有 {existing} 筆商品，跳過示意資料初始化。")
            return

        print("[seed_demo] Products 資料表為空，開始建立示意商品...")

        # ── 1. 建立示意賣家帳號 ──────────────────────────────────────────
        demo_seller = db.query(models.User).filter(
            models.User.Email == "demo@idoltrade.tw"
        ).first()

        if not demo_seller:
            demo_seller = models.User(
                Account="IdolTrade官方示意",
                Password="demo1234",
                Email="demo@idoltrade.tw",
                SellerReputation=5.00,
                BuyerReputation=5.00,
            )
            db.add(demo_seller)
            db.commit()
            db.refresh(demo_seller)

        seller_id = demo_seller.UserID

        # ── 2. 輔助函式：取得或建立 Group / Member ──────────────────────
        def get_or_create_group(name: str) -> models.Group:
            g = db.query(models.Group).filter(models.Group.GroupName == name).first()
            if not g:
                g = models.Group(GroupName=name)
                db.add(g)
                db.commit()
                db.refresh(g)
            return g

        def get_or_create_member(name: str, group_id: int) -> models.Member:
            m = db.query(models.Member).filter(
                models.Member.MemberName == name,
                models.Member.GroupID == group_id,
            ).first()
            if not m:
                m = models.Member(MemberName=name, GroupID=group_id)
                db.add(m)
                db.commit()
                db.refresh(m)
            return m

        def create_product(name, desc, price, method, image_file, seller_id) -> models.Product:
            p = models.Product(
                SellerID=seller_id,
                ProductName=name,
                Description=desc,
                Price=price,
                TradeMethod=method,
                Status="Available",
                ImageUrl=f"demo_products/{image_file}",
            )
            db.add(p)
            db.commit()
            db.refresh(p)
            return p

        def link_product_member(product_id: int, member_id: int):
            rel = models.ProductMemberRel(ProductID=product_id, MemberID=member_id)
            db.add(rel)
            db.commit()

        # ── 3. 建立 9 筆商品 ─────────────────────────────────────────────

        # 1. BLACKPINK Jisoo 小卡
        bp = get_or_create_group("BLACKPINK")
        jisoo = get_or_create_member("Jisoo", bp.GroupID)
        p1 = create_product(
            "BLACKPINK Jisoo 官方小卡",
            "BLACKPINK Born Pink 演唱會官方小卡，雷射亮面，保存良好，附保護套。9.5 成新。",
            350, "賣貨便", "bp_jisoo_card.jpg", seller_id
        )
        link_product_member(p1.ProductID, jisoo.MemberID)

        # 2. IVE Wonyoung 專輯
        ive = get_or_create_group("IVE")
        wonyoung = get_or_create_member("Wonyoung", ive.GroupID)
        p2 = create_product(
            "IVE Wonyoung 簽名版專輯",
            "IVE 1st World Tour『I'VE IVE』官方演唱會限定版專輯，Wonyoung 版本，附小卡全套。全新未拆。",
            1800, "郵寄", "ive_wonyoung_album.jpg", seller_id
        )
        link_product_member(p2.ProductID, wonyoung.MemberID)

        # 3. NewJeans OMG 海報
        nj = get_or_create_group("NewJeans")
        minji = get_or_create_member("Minji", nj.GroupID)
        hanni = get_or_create_member("Hanni", nj.GroupID)
        danielle = get_or_create_member("Danielle", nj.GroupID)
        haerin = get_or_create_member("Haerin", nj.GroupID)
        hyein = get_or_create_member("Hyein", nj.GroupID)
        p3 = create_product(
            "NewJeans OMG 全員官方海報",
            "NewJeans 'OMG' 單曲專輯官方海報，寬 51.5 × 長 72 cm，全員 Y2K 復古風格，無摺痕，全新。",
            450, "賣貨便", "newjeans_poster.jpg", seller_id
        )
        for m in [minji, hanni, danielle, haerin, hyein]:
            link_product_member(p3.ProductID, m.MemberID)

        # 4. aespa Karina 小卡
        ae = get_or_create_group("aespa")
        karina = get_or_create_member("Karina", ae.GroupID)
        p4 = create_product(
            "aespa Karina 雷射小卡",
            "aespa 'MY WORLD' 專輯 Karina 閃卡版本，質感極佳，全息雷射效果，近全新，附硬卡套。",
            280, "面交", "aespa_karina_card.jpg", seller_id
        )
        link_product_member(p4.ProductID, karina.MemberID)

        # 5. BTS Jungkook 手燈
        bts = get_or_create_group("BTS")
        jungkook = get_or_create_member("Jungkook", bts.GroupID)
        p5 = create_product(
            "BTS 官方 ARMY BOMB 應援手燈",
            "BTS ARMY BOMB Ver.4 官方演唱會手燈，支援 Weverse 連線功能，附原購買購物袋，極少使用。",
            2500, "郵寄", "bts_jungkook_lightstick.jpg", seller_id
        )
        link_product_member(p5.ProductID, jungkook.MemberID)

        # 6. SEVENTEEN 小卡套組
        svt = get_or_create_group("SEVENTEEN")
        scoups = get_or_create_member("S.Coups", svt.GroupID)
        jeonghan = get_or_create_member("Jeonghan", svt.GroupID)
        joshua = get_or_create_member("Joshua", svt.GroupID)
        p6 = create_product(
            "SEVENTEEN BE THE SUN 全員小卡套組",
            "SEVENTEEN 世界巡演《BE THE SUN》官方小卡套組，13 張全員，每張有保護套，完整收藏組。",
            980, "賣貨便", "seventeen_card_set.jpg", seller_id
        )
        for m in [scoups, jeonghan, joshua]:
            link_product_member(p6.ProductID, m.MemberID)

        # 7. LE SSERAFIM Chaewon 專輯
        lsf = get_or_create_group("LE SSERAFIM")
        chaewon = get_or_create_member("Chaewon", lsf.GroupID)
        p7 = create_product(
            "LE SSERAFIM UNFORGIVEN Chaewon 版",
            "LE SSERAFIM 1st Studio Album『UNFORGIVEN』Chaewon 版本，附亂數小卡 1 張，9 成新。",
            650, "郵寄", "lesserafim_chaewon_album.jpg", seller_id
        )
        link_product_member(p7.ProductID, chaewon.MemberID)

        # 8. BLACKPINK Rosé 海報
        rose = get_or_create_member("Rosé", bp.GroupID)
        p8 = create_product(
            "BLACKPINK Rosé 獨照豪華裱框海報",
            "BLACKPINK Rosé 金框裝裱藝術海報，A3 尺寸，玫瑰花卉精緻設計，送人或自用皆宜，限量發行。",
            500, "面交", "bp_rose_poster.jpg", seller_id
        )
        link_product_member(p8.ProductID, rose.MemberID)

        # 9. IVE Liz 明信片
        liz = get_or_create_member("Liz", ive.GroupID)
        p9 = create_product(
            "IVE Liz 限定明信片組",
            "IVE 粉絲見面會限定 Liz 明信片組，共 5 張，可愛插畫風格，粉絲手作品質，附粉紅緞帶包裝。",
            120, "賣貨便", "ive_liz_postcard.jpg", seller_id
        )
        link_product_member(p9.ProductID, liz.MemberID)

        print(f"[seed_demo] ✅ 成功建立 9 筆示意商品！賣家帳號 ID: {seller_id}")
        print("[seed_demo]    帳號: demo@idoltrade.tw / 密碼: demo1234")

    except Exception as e:
        db.rollback()
        print(f"[seed_demo] ❌ 初始化失敗: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # 手動執行重置：先清除再重新建立
    seed_demo_products()
