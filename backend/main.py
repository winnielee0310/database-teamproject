import shutil
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
UPLOAD_DIR = PROJECT_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Idol Merchandise Trading API",
    description="FastAPI backend for an idol merchandise trading demo.",
)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def product_to_response(product: models.Product) -> schemas.ProductResponse:
    member_names = []
    group_names = []

    for rel in product.members:
        if not rel.member:
            continue
        member_names.append(rel.member.MemberName)
        if rel.member.group:
            group_names.append(rel.member.group.GroupName)

    return schemas.ProductResponse(
        ProductID=product.ProductID,
        SellerID=product.SellerID,
        Price=float(product.Price),
        ProductName=product.ProductName,
        Description=product.Description,
        Condition=product.Condition,
        TradeMethod=product.TradeMethod,
        Status=product.Status,
        ImageUrl=product.ImageUrl,
        MemberNames=member_names,
        GroupNames=sorted(set(group_names)),
    )


def get_or_create_group(db: Session, group_name: str) -> models.Group:
    group = db.query(models.Group).filter(models.Group.GroupName == group_name).first()
    if group:
        return group

    group = models.Group(GroupName=group_name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_or_create_member(db: Session, group_id: int, member_name: str) -> models.Member:
    member = (
        db.query(models.Member)
        .filter(models.Member.GroupID == group_id, models.Member.MemberName == member_name)
        .first()
    )
    if member:
        return member

    member = models.Member(GroupID=group_id, MemberName=member_name)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@app.post("/auth/register", response_model=schemas.AuthResponse, tags=["Auth"])
def auth_register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User)
        .filter((models.User.Email == user.email) | (models.User.Account == user.username))
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already exists")

    db_user = models.User(Account=user.username, Password=user.password, Email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.AuthResponse(id=db_user.UserID, username=db_user.Account, email=db_user.Email)


@app.post("/auth/login", response_model=schemas.AuthResponse, tags=["Auth"])
def auth_login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.User)
        .filter(models.User.Email == user.email, models.User.Password == user.password)
        .first()
    )
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return schemas.AuthResponse(id=db_user.UserID, username=db_user.Account, email=db_user.Email)


@app.post("/users/", response_model=schemas.UserResponse, tags=["Users"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User)
        .filter((models.User.Email == user.Email) | (models.User.Account == user.Account))
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or account already exists")

    db_user = models.User(Account=user.Account, Password=user.Password, Email=user.Email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/{user_id}/reputation", tags=["Users"])
def get_seller_reputation(user_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            func.avg(models.Review.PackingScore).label("avg_packing"),
            func.avg(models.Review.VideoScore).label("avg_video"),
            func.avg(models.Review.SpeedScore).label("avg_speed"),
        )
        .join(models.Order, models.Review.OrderID == models.Order.OrderID)
        .join(models.Product, models.Order.ProductID == models.Product.ProductID)
        .filter(models.Product.SellerID == user_id)
        .first()
    )

    if not result or result.avg_packing is None:
        return {
            "SellerID": user_id,
            "Average_Packing": 5.0,
            "Average_Video": 5.0,
            "Average_Speed": 5.0,
            "Total_Reputation": 5.0,
        }

    total_score = (result.avg_packing + result.avg_video + result.avg_speed) / 3
    return {
        "SellerID": user_id,
        "Average_Packing": round(float(result.avg_packing), 2),
        "Average_Video": round(float(result.avg_video), 2),
        "Average_Speed": round(float(result.avg_speed), 2),
        "Total_Reputation": round(float(total_score), 2),
    }


@app.get("/users/{user_id}/sold_products", response_model=List[schemas.ProductResponse], tags=["Users"])
def get_user_sold_products(user_id: int, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.SellerID == user_id).all()
    return [product_to_response(product) for product in products]


@app.get("/users/{user_id}/bought_orders", tags=["Users"])
def get_user_bought_orders(user_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(models.Order, models.Product)
        .join(models.Product, models.Order.ProductID == models.Product.ProductID)
        .filter(models.Order.BuyerID == user_id)
        .all()
    )
    return [
        {
            "OrderID": order.OrderID,
            "ProductID": product.ProductID,
            "OrderPrice": float(order.OrderPrice),
            "OrderDate": order.OrderDate,
            "Status": order.Status,
            "ProductName": product.ProductName,
            "Description": product.Description,
            "ImageUrl": product.ImageUrl,
        }
        for order, product in rows
    ]


@app.get("/groups/", response_model=List[schemas.GroupResponse], tags=["Idols"])
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).order_by(models.Group.GroupName).all()


@app.get("/groups/{group_id}/members", response_model=List[schemas.MemberResponse], tags=["Idols"])
def get_group_members(group_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Member)
        .filter(models.Member.GroupID == group_id)
        .order_by(models.Member.MemberName)
        .all()
    )


@app.get("/members/", response_model=List[schemas.MemberResponse], tags=["Idols"])
def get_all_members(db: Session = Depends(get_db)):
    return db.query(models.Member).order_by(models.Member.MemberName).all()


@app.post("/products/", response_model=schemas.ProductResponse, tags=["Products"])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    seller = db.query(models.User).filter(models.User.UserID == product.SellerID).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    db_product = models.Product(
        SellerID=product.SellerID,
        Price=product.Price,
        ProductName=product.ProductName,
        Description=product.Description,
        Condition=product.Condition,
        TradeMethod=product.TradeMethod,
        ImageUrl=product.ImageUrl,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    final_member_ids = list(product.MemberIDs)

    if product.CustomGroupName and product.CustomMemberNames:
        group = get_or_create_group(db, product.CustomGroupName.strip())
        for member_name in product.CustomMemberNames:
            member_name = member_name.strip()
            if not member_name:
                continue
            member = get_or_create_member(db, group.GroupID, member_name)
            final_member_ids.append(member.MemberID)

    for member_id in sorted(set(final_member_ids)):
        member = db.query(models.Member).filter(models.Member.MemberID == member_id).first()
        if member:
            db.add(models.ProductMemberRel(ProductID=db_product.ProductID, MemberID=member_id))

    db.commit()
    db.refresh(db_product)
    return product_to_response(db_product)


@app.get("/products/search", response_model=List[schemas.ProductResponse], tags=["Products"])
def search_products(
    member_name: Optional[str] = None,
    group_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Product).filter(models.Product.Status == "Available")

    if member_name or group_name:
        query = query.join(
            models.ProductMemberRel,
            models.Product.ProductID == models.ProductMemberRel.ProductID,
        ).join(
            models.Member,
            models.ProductMemberRel.MemberID == models.Member.MemberID,
        )

    if member_name:
        query = query.filter(models.Member.MemberName.ilike(f"%{member_name}%"))

    if group_name:
        query = query.join(
            models.Group,
            models.Member.GroupID == models.Group.GroupID,
        ).filter(models.Group.GroupName.ilike(f"%{group_name}%"))

    products = query.distinct().order_by(models.Product.ProductID.desc()).all()
    return [product_to_response(product) for product in products]


@app.post("/upload-image/", tags=["Products"])
def upload_image(file: UploadFile = File(...)):
    original_name = Path(file.filename or "upload").name
    ext = Path(original_name).suffix
    filename = f"{uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"ImageUrl": filename, "filename": filename}


@app.post("/wishlists/", response_model=schemas.WishlistResponse, tags=["Wishlist"])
def add_to_wishlist(wish: schemas.WishlistCreate, db: Session = Depends(get_db)):
    member_id = wish.MemberID

    if wish.CustomMemberName:
        group_name = (wish.CustomGroupName or "Unknown Group").strip()
        group = get_or_create_group(db, group_name)
        member = get_or_create_member(db, group.GroupID, wish.CustomMemberName.strip())
        member_id = member.MemberID

    if not member_id:
        raise HTTPException(status_code=400, detail="Missing member information")

    user = db.query(models.User).filter(models.User.UserID == wish.UserID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_wish = models.Wishlist(
        UserID=wish.UserID,
        MemberID=member_id,
        MaxPrice=wish.MaxPrice,
        ConditionReq=wish.ConditionReq,
    )
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    return db_wish


@app.get("/users/{user_id}/wishlists", response_model=List[schemas.WishlistResponse], tags=["Wishlist"])
def get_user_wishlists(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Wishlist).filter(models.Wishlist.UserID == user_id).all()


@app.post("/orders/", response_model=schemas.OrderResponse, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product)
        .filter(models.Product.ProductID == order.ProductID)
        .with_for_update()
        .first()
    )

    if not product or product.Status != "Available":
        raise HTTPException(status_code=400, detail="Product is not available")
    if product.SellerID == order.BuyerID:
        raise HTTPException(status_code=400, detail="Seller cannot buy their own product")

    db_order = models.Order(
        BuyerID=order.BuyerID,
        ProductID=order.ProductID,
        OrderPrice=product.Price,
        Status="Completed",
    )
    db.add(db_order)
    product.Status = "Sold"
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

    existing_review = db.query(models.Review).filter(models.Review.OrderID == review.OrderID).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="This order already has a review")

    db_review = models.Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@app.post("/messages/", response_model=schemas.MessageResponse, tags=["Messages"])
def send_product_message(msg: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_msg = models.ProductMessage(**msg.model_dump())
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


@app.get("/products/{product_id}/messages", response_model=List[schemas.MessageResponse], tags=["Messages"])
def get_product_messages(product_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.ProductMessage)
        .filter(models.ProductMessage.ProductID == product_id)
        .order_by(models.ProductMessage.SentAt)
        .all()
    )


@app.post("/chats/create", response_model=schemas.ChatResponse, tags=["Chats"])
def create_chat(chat_data: schemas.ChatCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.ProductID == chat_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if chat_data.buyer_id == chat_data.seller_id:
        raise HTTPException(status_code=400, detail="Buyer and seller must be different")

    existing_chat = (
        db.query(models.Chat)
        .filter(
            models.Chat.ProductID == chat_data.product_id,
            models.Chat.BuyerID == chat_data.buyer_id,
            models.Chat.SellerID == chat_data.seller_id,
        )
        .first()
    )
    if existing_chat:
        return schemas.ChatResponse(chat_id=existing_chat.ChatID)

    db_chat = models.Chat(
        ProductID=chat_data.product_id,
        BuyerID=chat_data.buyer_id,
        SellerID=chat_data.seller_id,
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return schemas.ChatResponse(chat_id=db_chat.ChatID)


@app.post("/messages/send", tags=["Chats"])
def send_chat_message(msg_data: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    chat = db.query(models.Chat).filter(models.Chat.ChatID == msg_data.chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    db_msg = models.ChatMessage(
        ChatID=msg_data.chat_id,
        SenderID=msg_data.sender_id,
        Message=msg_data.message,
    )
    db.add(db_msg)
    db.commit()
    return {"status": "success"}


@app.post("/chats/{chat_id}/read", tags=["Chats"])
def mark_chat_messages_as_read(chat_id: int, user_id: int, db: Session = Depends(get_db)):
    db.query(models.ChatMessage).filter(
        models.ChatMessage.ChatID == chat_id,
        models.ChatMessage.SenderID != user_id,
        models.ChatMessage.IsRead == False,  # noqa: E712
    ).update({"IsRead": True})
    db.commit()
    return {"status": "success"}


@app.get("/messages/{chat_id}", response_model=List[schemas.ChatMessageResponse], tags=["Chats"])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.ChatID == chat_id)
        .order_by(models.ChatMessage.CreatedAt)
        .all()
    )
    return [
        schemas.ChatMessageResponse(
            id=message.MessageID,
            sender_id=message.SenderID,
            message=message.Message,
            created_at=message.CreatedAt,
            is_read=bool(message.IsRead),
        )
        for message in messages
    ]


@app.get("/users/{user_id}/chats", response_model=List[schemas.ChatListResponse], tags=["Chats"])
def get_user_chats(user_id: int, db: Session = Depends(get_db)):
    chats = (
        db.query(models.Chat)
        .filter((models.Chat.BuyerID == user_id) | (models.Chat.SellerID == user_id))
        .all()
    )

    result = []
    for chat in chats:
        product_name = chat.product.ProductName if chat.product else "Unknown Product"
        last_msg = (
            db.query(models.ChatMessage)
            .filter(models.ChatMessage.ChatID == chat.ChatID)
            .order_by(models.ChatMessage.CreatedAt.desc())
            .first()
        )
        unread_count = (
            db.query(models.ChatMessage)
            .filter(
                models.ChatMessage.ChatID == chat.ChatID,
                models.ChatMessage.SenderID != user_id,
                models.ChatMessage.IsRead == False,  # noqa: E712
            )
            .count()
        )
        result.append(
            schemas.ChatListResponse(
                chat_id=chat.ChatID,
                product_name=product_name,
                last_message=last_msg.Message if last_msg else "",
                updated_at=last_msg.CreatedAt if last_msg else chat.CreatedAt,
                unread_count=unread_count,
            )
        )

    result.sort(key=lambda item: item.updated_at, reverse=True)
    return result


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Idol Merchandise Trading API"}
