from database import SessionLocal
import models


DEMO_PRODUCTS = [
    {
        "group": "BLACKPINK",
        "member": "Jisoo",
        "name": "BLACKPINK Jisoo photocard",
        "description": "Official Jisoo photocard in good condition.",
        "price": 350,
        "condition": "Used - Good",
        "method": "Shipping",
        "image": "demo_products/bp_jisoo_card.jpg",
    },
    {
        "group": "IVE",
        "member": "Wonyoung",
        "name": "IVE Wonyoung album inclusions",
        "description": "Album inclusions bundle with photocard and postcard.",
        "price": 800,
        "condition": "Like New",
        "method": "Meetup",
        "image": "demo_products/ive_wonyoung_album.jpg",
    },
    {
        "group": "aespa",
        "member": "Karina",
        "name": "aespa Karina photocard",
        "description": "Karina photocard with sleeve.",
        "price": 280,
        "condition": "New",
        "method": "Mailing",
        "image": "demo_products/aespa_karina_card.jpg",
    },
]


def get_or_create_group(db, name):
    group = db.query(models.Group).filter(models.Group.GroupName == name).first()
    if group:
        return group

    group = models.Group(GroupName=name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_or_create_member(db, group_id, name):
    member = (
        db.query(models.Member)
        .filter(models.Member.GroupID == group_id, models.Member.MemberName == name)
        .first()
    )
    if member:
        return member

    member = models.Member(GroupID=group_id, MemberName=name)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def seed_demo_products():
    db = SessionLocal()
    try:
        seller = db.query(models.User).filter(models.User.Email == "demo@example.com").first()
        if not seller:
            seller = models.User(
                Account="demo_user",
                Password="demo1234",
                Email="demo@example.com",
                SellerReputation=5.00,
                BuyerReputation=5.00,
            )
            db.add(seller)
            db.commit()
            db.refresh(seller)

        for item in DEMO_PRODUCTS:
            exists = (
                db.query(models.Product)
                .filter(models.Product.ProductName == item["name"])
                .first()
            )
            if exists:
                continue

            group = get_or_create_group(db, item["group"])
            member = get_or_create_member(db, group.GroupID, item["member"])
            product = models.Product(
                SellerID=seller.UserID,
                ProductName=item["name"],
                Description=item["description"],
                Price=item["price"],
                Condition=item["condition"],
                TradeMethod=item["method"],
                Status="Available",
                ImageUrl=item["image"],
            )
            db.add(product)
            db.commit()
            db.refresh(product)
            db.add(
                models.ProductMemberRel(
                    ProductID=product.ProductID,
                    MemberID=member.MemberID,
                )
            )
            db.commit()

        print("Demo products are ready.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_products()
