from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models, schemas
from database import engine, get_db
import os
import shutil
from fastapi.staticfiles import StaticFiles

os.makedirs("uploads", exist_ok=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="偶像周邊二手交易與訂單管理系統 API", description="基於實體關係圖(ERD)完整設計的交易系統")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

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

@app.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

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

@app.get("/users/{user_id}/sold_products", response_model=List[schemas.ProductResponse], tags=["Users"])
def get_user_sold_products(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Product).filter(models.Product.SellerID == user_id).all()

@app.get("/users/{user_id}/bought_orders", tags=["Users"])
def get_user_bought_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(models.Order, models.Product).join(models.Product).filter(models.Order.BuyerID == user_id).all()
    res = []
    for o, p in orders:
        res.append({
            "OrderID": o.OrderID,
            "ProductID": p.ProductID,
            "OrderPrice": o.OrderPrice,
            "OrderDate": o.OrderDate,
            "Status": o.Status,
            "ProductName": p.ProductName,
            "Description": p.Description,
            "ImageUrl": p.ImageUrl
        })
    return res

@app.get("/users/{user_id}/notifications", response_model=List[schemas.MessageResponse], tags=["Users"])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Message).filter(models.Message.ReceiverID == user_id).order_by(models.Message.SentAt.desc()).limit(10).all()

# ===============================
# 2. 團體與成員模組 (Group & Member)
# ===============================
@app.get("/groups/", response_model=List[schemas.GroupResponse], tags=["Idols"])
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()

@app.get("/groups/{group_id}/members", response_model=List[schemas.MemberResponse], tags=["Idols"])
def get_group_members(group_id: int, db: Session = Depends(get_db)):
    return db.query(models.Member).filter(models.Member.GroupID == group_id).all()

@app.get("/members/", response_model=List[schemas.MemberResponse], tags=["Idols"])
def get_all_members(db: Session = Depends(get_db)):
    return db.query(models.Member).all()

# ===============================
# 3. 商品與搜尋模組 (Product)
# ===============================
@app.post("/products/", response_model=schemas.ProductResponse, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        SellerID=product.SellerID, Price=product.Price,
        ProductName=product.ProductName, Description=product.Description, TradeMethod=product.TradeMethod,
        ImageUrl=product.ImageUrl
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    final_member_ids = list(product.MemberIDs) if product.MemberIDs else []
    
    if product.CustomGroupName and product.CustomMemberNames:
        group = db.query(models.Group).filter(models.Group.GroupName == product.CustomGroupName).first()
        if not group:
            group = models.Group(GroupName=product.CustomGroupName)
            db.add(group)
            db.commit()
            db.refresh(group)
            
        for m_name in product.CustomMemberNames:
            m_name = m_name.strip()
            if not m_name: continue
            member = db.query(models.Member).filter(models.Member.MemberName == m_name, models.Member.GroupID == group.GroupID).first()
            if not member:
                member = models.Member(MemberName=m_name, GroupID=group.GroupID)
                db.add(member)
                db.commit()
                db.refresh(member)
            final_member_ids.append(member.MemberID)
            
    # N:M 關聯寫入 (商品標記成員)
    for member_id in final_member_ids:
        rel = models.ProductMemberRel(ProductID=db_product.ProductID, MemberID=member_id)
        db.add(rel)
    db.commit()
    
    # 願望清單自動撮合比對 (貨找人)
    if final_member_ids:
        matched_wishes = db.query(models.Wishlist).filter(
            models.Wishlist.MemberID.in_(final_member_ids),
            models.Wishlist.MaxPrice >= product.Price
        ).all()
        print(f"系統自動比對：找到 {len(matched_wishes)} 名買家的願望清單符合此周邊！")
    
    return db_product

@app.get("/products/search", response_model=List[schemas.ProductResponse], tags=["Products"])
def search_products(member_name: str = None, group_name: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Product).join(models.ProductMemberRel)
    
    if member_name or group_name:
        query = query.join(models.Member, models.ProductMemberRel.MemberID == models.Member.MemberID)
        
    if member_name:
        query = query.filter(models.Member.MemberName.ilike(f"%{member_name}%"))
        
    if group_name:
        query = query.join(models.Group, models.Member.GroupID == models.Group.GroupID)
        query = query.filter(models.Group.GroupName.ilike(f"%{group_name}%"))
        
    products = query.filter(models.Product.Status == "Available").all()
    res = []
    for p in products:
        m_names = [m.member.MemberName for m in p.members if m.member]
        g_names = list(set([m.member.group.GroupName for m in p.members if m.member and m.member.group]))
        res.append({
            "ProductID": p.ProductID,
            "SellerID": p.SellerID,
            "Price": p.Price,
            "ProductName": p.ProductName, "Description": p.Description,
            "TradeMethod": p.TradeMethod,
            "Status": p.Status,
            "ImageUrl": p.ImageUrl,
            "MemberNames": m_names,
            "GroupNames": g_names
        })
    return res

@app.post("/upload-image/", tags=["Products"])
def upload_image(file: UploadFile = File(...)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"ImageUrl": file.filename, "filename": file.filename}

# ===============================
# 4. 願望清單模組 (Wishlist)
# ===============================
@app.post("/wishlists/", response_model=schemas.WishlistResponse, tags=["Wishlist"])
def add_to_wishlist(wish: schemas.WishlistCreate, db: Session = Depends(get_db)):
    member_id = wish.MemberID
    
    if wish.CustomMemberName:
        group_name = wish.CustomGroupName or "Unknown Group"
        group = db.query(models.Group).filter(models.Group.GroupName == group_name).first()
        if not group:
            group = models.Group(GroupName=group_name)
            db.add(group)
            db.commit()
            db.refresh(group)
        
        member = db.query(models.Member).filter(models.Member.MemberName == wish.CustomMemberName, models.Member.GroupID == group.GroupID).first()
        if not member:
            member = models.Member(MemberName=wish.CustomMemberName, GroupID=group.GroupID)
            db.add(member)
            db.commit()
            db.refresh(member)
        member_id = member.MemberID

    if not member_id:
        raise HTTPException(status_code=400, detail="Missing member information")
        
    db_wish = models.Wishlist(UserID=wish.UserID, MemberID=member_id, MaxPrice=wish.MaxPrice, ConditionReq=wish.ConditionReq)
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

@app.get("/users/{user_id}/orders", response_model=List[schemas.OrderResponse], tags=["Orders"])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.BuyerID == user_id).all()

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

# ===============================
# 6. 對話系統模組 (Messaging)
# ===============================
@app.post("/messages/", response_model=schemas.MessageResponse, tags=["Messages"])
def send_message(msg: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_msg = models.Message(**msg.model_dump())
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

@app.get("/products/{product_id}/messages", response_model=List[schemas.MessageResponse], tags=["Messages"])
def get_product_messages(product_id: int, db: Session = Depends(get_db)):
    return db.query(models.Message).filter(models.Message.ProductID == product_id).order_by(models.Message.SentAt).all()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Idol Merchandise Trading API"}
