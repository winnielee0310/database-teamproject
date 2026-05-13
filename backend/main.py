from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import models, schemas
from database import engine, get_db

# 建立所有的資料表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="偶像周邊二手交易與訂單管理系統 API")

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允許所有前端來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/products/", response_model=schemas.ProductResponse, summary="多維度商品上架")
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # 1. 建立商品
    db_product = models.Product(
        SellerID=product.SellerID,
        Price=product.Price,
        Condition=product.Condition,
        TradeMethod=product.TradeMethod
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # 2. 建立關聯表 (解決 N:M)
    for member_id in product.MemberIDs:
        rel = models.ProductMemberRel(ProductID=db_product.ProductID, MemberID=member_id)
        db.add(rel)
    db.commit()
    
    # 3. 願望清單自動撮合 (貨找人)
    # 找尋是否有買家想要這個成員的商品，且預算足夠、狀態符合
    matched_wishes = db.query(models.Wishlist).filter(
        models.Wishlist.MemberID.in_(product.MemberIDs),
        models.Wishlist.MaxPrice >= product.Price
    ).all()
    
    # TODO: 實務上這裡可以透過 Webhook 或 Email 發送通知給符合條件的 UserID
    print(f"找到 {len(matched_wishes)} 筆符合條件的願望清單！")
    
    return db_product

@app.get("/products/search", summary="精確搜尋特定成員周邊 (包含多成員卡)")
def search_products_by_member(member_id: int, db: Session = Depends(get_db)):
    # 透過 JOIN 篩選出包含該成員的所有品項
    products = db.query(models.Product).join(models.ProductMemberRel).filter(
        models.ProductMemberRel.MemberID == member_id,
        models.Product.Status == "Available"
    ).all()
    return products

@app.post("/orders/", summary="建立訂單並扣除庫存(悲觀鎖概念)")
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # 使用 with_for_update 實作悲觀鎖避免超賣 Race Condition
    product = db.query(models.Product).filter(
        models.Product.ProductID == order.ProductID
    ).with_for_update().first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.Status != "Available":
        raise HTTPException(status_code=400, detail="Product is already sold or removed")
        
    # 建立訂單，並產生歷史快照價格
    db_order = models.Order(
        BuyerID=order.BuyerID,
        ProductID=order.ProductID,
        OrderPrice=product.Price,
        Status="Pending"
    )
    db.add(db_order)
    
    # 軟刪除商品，將狀態改為 Sold
    product.Status = "Sold"
    db.add(product)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/users/{user_id}/reputation", summary="查詢並動態計算賣家信譽評分")
def get_seller_reputation(user_id: int, db: Session = Depends(get_db)):
    # 聚合查詢 (GROUP BY 概念)
    # 取得這個賣家所有已售出訂單的評價平均
    # (實務上可以定期排程寫回 User 表，這裡示範即時動態計算)
    result = db.query(
        func.avg(models.Review.PackingScore).label('avg_packing'),
        func.avg(models.Review.VideoScore).label('avg_video'),
        func.avg(models.Review.SpeedScore).label('avg_speed')
    ).join(models.Order).join(models.Product).filter(
        models.Product.SellerID == user_id
    ).first()
    
    if not result.avg_packing:
        return {"message": "No reviews yet", "reputation": 5.0}
        
    total_score = (result.avg_packing + result.avg_video + result.avg_speed) / 3
    return {
        "SellerID": user_id,
        "Average_Packing": round(result.avg_packing, 2),
        "Average_Video": round(result.avg_video, 2),
        "Average_Speed": round(result.avg_speed, 2),
        "Total_Reputation": round(total_score, 2)
    }

@app.get("/", summary="Root")
def read_root():
    return {"message": "Welcome to Idol Merchandise Trading API"}
