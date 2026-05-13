from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="偶像周邊二手交易與訂單管理系統 API", description="基於實體關係圖(ERD)完整設計的交易系統")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# 1. 使用者與信譽模組 (User & Reputation)
# ===============================
@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(Account=user.Account, Password=user.Password, Email=user.Email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}/reputation", tags=["Users"])
def get_seller_reputation(user_id: int, db: Session = Depends(get_db)):
    # SQL 聚合查詢: 計算該賣家歷史訂單評價
    result = db.query(
        func.avg(models.Review.PackingScore).label('avg_packing'),
        func.avg(models.Review.VideoScore).label('avg_video'),
        func.avg(models.Review.SpeedScore).label('avg_speed')
    ).join(models.Order).join(models.Product).filter(
        models.Product.SellerID == user_id
    ).first()
    
    if not result.avg_packing:
        return {"message": "尚無評價", "reputation": 5.0}
        
    total_score = (result.avg_packing + result.avg_video + result.avg_speed) / 3
    return {
        "SellerID": user_id,
        "Average_Packing": round(result.avg_packing, 2),
        "Average_Video": round(result.avg_video, 2),
        "Average_Speed": round(result.avg_speed, 2),
        "Total_Reputation": round(total_score, 2)
    }

# ===============================
# 2. 團體與成員模組 (Group & Member)
# ===============================
@app.get("/groups/", response_model=List[schemas.GroupResponse], tags=["Idols"])
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()

@app.get("/groups/{group_id}/members", response_model=List[schemas.MemberResponse], tags=["Idols"])
def get_group_members(group_id: int, db: Session = Depends(get_db)):
    return db.query(models.Member).filter(models.Member.GroupID == group_id).all()

# ===============================
# 3. 商品與搜尋模組 (Product)
# ===============================
@app.post("/products/", response_model=schemas.ProductResponse, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        SellerID=product.SellerID, Price=product.Price,
        Condition=product.Condition, TradeMethod=product.TradeMethod
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # N:M 關聯寫入 (商品標記成員)
    for member_id in product.MemberIDs:
        rel = models.ProductMemberRel(ProductID=db_product.ProductID, MemberID=member_id)
        db.add(rel)
    db.commit()
    
    # 願望清單自動撮合比對 (貨找人)
    matched_wishes = db.query(models.Wishlist).filter(
        models.Wishlist.MemberID.in_(product.MemberIDs),
        models.Wishlist.MaxPrice >= product.Price
    ).all()
    print(f"系統自動比對：找到 {len(matched_wishes)} 名買家的願望清單符合此周邊！")
    
    return db_product

@app.get("/products/search", response_model=List[schemas.ProductResponse], tags=["Products"])
def search_products(member_id: int, db: Session = Depends(get_db)):
    return db.query(models.Product).join(models.ProductMemberRel).filter(
        models.ProductMemberRel.MemberID == member_id,
        models.Product.Status == "Available"
    ).all()

# ===============================
# 4. 願望清單模組 (Wishlist)
# ===============================
@app.post("/wishlists/", response_model=schemas.WishlistResponse, tags=["Wishlist"])
def add_to_wishlist(wish: schemas.WishlistCreate, db: Session = Depends(get_db)):
    db_wish = models.Wishlist(**wish.model_dump())
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    return db_wish

@app.get("/users/{user_id}/wishlists", response_model=List[schemas.WishlistResponse], tags=["Wishlist"])
def get_user_wishlists(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Wishlist).filter(models.Wishlist.UserID == user_id).all()

# ===============================
# 5. 訂單與評價模組 (Order & Review)
# ===============================
@app.post("/orders/", response_model=schemas.OrderResponse, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # 悲觀鎖 (Pessimistic Locking) 避免限量小卡超賣
    product = db.query(models.Product).filter(
        models.Product.ProductID == order.ProductID
    ).with_for_update().first()
    
    if not product or product.Status != "Available":
        raise HTTPException(status_code=400, detail="商品不存在或已售出")
        
    db_order = models.Order(
        BuyerID=order.BuyerID,
        ProductID=order.ProductID,
        OrderPrice=product.Price, # 歷史快照
        Status="Completed"
    )
    db.add(db_order)
    
    product.Status = "Sold" # 軟刪除
    db.add(product)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.post("/reviews/", response_model=schemas.ReviewResponse, tags=["Orders"])
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.OrderID == review.OrderID).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    db_review = models.Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Idol Merchandise Trading API"}
