from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "User"

    UserID = Column("使用者編號", Integer, primary_key=True, index=True, autoincrement=True)
    Account = Column("帳號", String(50), unique=True, nullable=False)
    Password = Column("密碼", String(255), nullable=False)
    Email = Column("電子郵件", String(100), unique=True, nullable=False)
    SellerReputation = Column("賣家評價", DECIMAL(3, 2), default=5.00)
    BuyerReputation = Column("買家評價", DECIMAL(3, 2), default=5.00)


class Group(Base):
    __tablename__ = "Group"

    GroupID = Column("團體編號", Integer, primary_key=True, index=True, autoincrement=True)
    GroupName = Column("團體名稱", String(100), nullable=False)
    Company = Column("公司", String(100))


class Member(Base):
    __tablename__ = "Member"

    MemberID = Column("成員編號", Integer, primary_key=True, index=True, autoincrement=True)
    GroupID = Column("團體編號", Integer, ForeignKey("Group.團體編號", ondelete="CASCADE"), nullable=False)
    MemberName = Column("成員名稱", String(100), nullable=False)

    group = relationship("Group")


class Product(Base):
    __tablename__ = "Product"

    ProductID = Column("商品編號", Integer, primary_key=True, index=True, autoincrement=True)
    SellerID = Column("賣家編號", Integer, ForeignKey("User.使用者編號"), nullable=False)
    Price = Column("價格", DECIMAL(10, 2), nullable=False)
    ProductName = Column("商品名稱", String(100), nullable=False)
    Description = Column("商品描述", Text, nullable=True)
    Condition = Column("商品狀況", String(50), nullable=False)
    TradeMethod = Column("交易方式", String(50), nullable=False)
    Status = Column("狀態", String(20), default="Available")
    ImageUrl = Column("圖片網址", String(255), nullable=True)

    seller = relationship("User")
    members = relationship(
        "ProductMemberRel",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductMemberRel(Base):
    __tablename__ = "Product_Member_Rel"

    RelID = Column("關聯編號", Integer, primary_key=True, index=True, autoincrement=True)
    ProductID = Column("商品編號", Integer, ForeignKey("Product.商品編號", ondelete="CASCADE"), nullable=False)
    MemberID = Column("成員編號", Integer, ForeignKey("Member.成員編號", ondelete="CASCADE"), nullable=False)

    product = relationship("Product", back_populates="members")
    member = relationship("Member")


class Order(Base):
    __tablename__ = "Order"

    OrderID = Column("訂單編號", Integer, primary_key=True, index=True, autoincrement=True)
    BuyerID = Column("買家編號", Integer, ForeignKey("User.使用者編號"), nullable=False)
    ProductID = Column("商品編號", Integer, ForeignKey("Product.商品編號"), unique=True, nullable=False)
    OrderPrice = Column("訂單金額", DECIMAL(10, 2), nullable=False)
    Status = Column("狀態", String(20), default="Pending")
    OrderDate = Column("訂單日期", DateTime, default=datetime.utcnow)


class Wishlist(Base):
    __tablename__ = "Wishlist"

    WishID = Column("願望編號", Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column("使用者編號", Integer, ForeignKey("User.使用者編號", ondelete="CASCADE"), nullable=False)
    MemberID = Column("成員編號", Integer, ForeignKey("Member.成員編號", ondelete="CASCADE"), nullable=False)
    MaxPrice = Column("最高價格", DECIMAL(10, 2), nullable=False)
    ConditionReq = Column("狀況需求", String(50))


class Review(Base):
    __tablename__ = "Review"

    ReviewID = Column("評價編號", Integer, primary_key=True, index=True, autoincrement=True)
    OrderID = Column("訂單編號", Integer, ForeignKey("Order.訂單編號", ondelete="CASCADE"), unique=True, nullable=False)
    PackingScore = Column("包裝分數", Integer, nullable=False)
    VideoScore = Column("影片分數", Integer, nullable=False)
    SpeedScore = Column("速度分數", Integer, nullable=False)
    Comment = Column("評論", Text)


class ProductMessage(Base):
    __tablename__ = "ProductMessage"

    MessageID = Column("訊息編號", Integer, primary_key=True, index=True, autoincrement=True)
    ProductID = Column("商品編號", Integer, ForeignKey("Product.商品編號", ondelete="CASCADE"), nullable=False)
    SenderID = Column("發送者編號", Integer, ForeignKey("User.使用者編號"), nullable=False)
    ReceiverID = Column("接收者編號", Integer, ForeignKey("User.使用者編號"), nullable=False)
    Content = Column("內容", Text, nullable=False)
    MediaUrl = Column("媒體網址", String(255), nullable=True)
    SentAt = Column("發送時間", DateTime, default=datetime.utcnow)

    product = relationship("Product")
    sender = relationship("User", foreign_keys=[SenderID])
    receiver = relationship("User", foreign_keys=[ReceiverID])


class Chat(Base):
    __tablename__ = "Chat"

    ChatID = Column("聊天室編號", Integer, primary_key=True, index=True, autoincrement=True)
    ProductID = Column("商品編號", Integer, ForeignKey("Product.商品編號", ondelete="CASCADE"), nullable=False)
    BuyerID = Column("買家編號", Integer, ForeignKey("User.使用者編號"), nullable=False)
    SellerID = Column("賣家編號", Integer, ForeignKey("User.使用者編號"), nullable=False)
    CreatedAt = Column("建立時間", DateTime, default=datetime.utcnow)

    product = relationship("Product")
    messages = relationship(
        "ChatMessage",
        back_populates="chat",
        cascade="all, delete-orphan",
    )


class ChatMessage(Base):
    __tablename__ = "ChatMessage"

    MessageID = Column("訊息編號", Integer, primary_key=True, index=True, autoincrement=True)
    ChatID = Column("聊天室編號", Integer, ForeignKey("Chat.聊天室編號", ondelete="CASCADE"), nullable=False)
    SenderID = Column("發送者編號", Integer, ForeignKey("User.使用者編號"), nullable=False)
    Message = Column("訊息內容", Text, nullable=False)
    IsRead = Column("是否已讀", Boolean, default=False)
    CreatedAt = Column("建立時間", DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
