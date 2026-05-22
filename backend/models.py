from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "User"

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Account = Column(String(50), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    SellerReputation = Column(DECIMAL(3, 2), default=5.00)
    BuyerReputation = Column(DECIMAL(3, 2), default=5.00)


class Group(Base):
    __tablename__ = "Group"

    GroupID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    GroupName = Column(String(100), nullable=False)
    Company = Column(String(100))


class Member(Base):
    __tablename__ = "Member"

    MemberID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    GroupID = Column(Integer, ForeignKey("Group.GroupID", ondelete="CASCADE"), nullable=False)
    MemberName = Column(String(100), nullable=False)

    group = relationship("Group")


class Product(Base):
    __tablename__ = "Product"

    ProductID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    SellerID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    ProductName = Column(String(100), nullable=False)
    Description = Column(Text, nullable=True)
    Condition = Column(String(50), nullable=False)
    TradeMethod = Column(String(50), nullable=False)
    Status = Column(String(20), default="Available")
    ImageUrl = Column(String(255), nullable=True)

    seller = relationship("User")
    members = relationship(
        "ProductMemberRel",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductMemberRel(Base):
    __tablename__ = "Product_Member_Rel"

    RelID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ProductID = Column(Integer, ForeignKey("Product.ProductID", ondelete="CASCADE"), nullable=False)
    MemberID = Column(Integer, ForeignKey("Member.MemberID", ondelete="CASCADE"), nullable=False)

    product = relationship("Product", back_populates="members")
    member = relationship("Member")


class Order(Base):
    __tablename__ = "Order"

    OrderID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    BuyerID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    ProductID = Column(Integer, ForeignKey("Product.ProductID"), unique=True, nullable=False)
    OrderPrice = Column(DECIMAL(10, 2), nullable=False)
    Status = Column(String(20), default="Pending")
    OrderDate = Column(DateTime, default=datetime.utcnow)


class Wishlist(Base):
    __tablename__ = "Wishlist"

    WishID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID", ondelete="CASCADE"), nullable=False)
    MemberID = Column(Integer, ForeignKey("Member.MemberID", ondelete="CASCADE"), nullable=False)
    MaxPrice = Column(DECIMAL(10, 2), nullable=False)
    ConditionReq = Column(String(50))


class Review(Base):
    __tablename__ = "Review"

    ReviewID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey("Order.OrderID", ondelete="CASCADE"), unique=True, nullable=False)
    PackingScore = Column(Integer, nullable=False)
    VideoScore = Column(Integer, nullable=False)
    SpeedScore = Column(Integer, nullable=False)
    Comment = Column(Text)


class ProductMessage(Base):
    __tablename__ = "ProductMessage"

    MessageID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ProductID = Column(Integer, ForeignKey("Product.ProductID", ondelete="CASCADE"), nullable=False)
    SenderID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    ReceiverID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    Content = Column(Text, nullable=False)
    MediaUrl = Column(String(255), nullable=True)
    SentAt = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product")
    sender = relationship("User", foreign_keys=[SenderID])
    receiver = relationship("User", foreign_keys=[ReceiverID])


class Chat(Base):
    __tablename__ = "Chat"

    ChatID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ProductID = Column(Integer, ForeignKey("Product.ProductID", ondelete="CASCADE"), nullable=False)
    BuyerID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    SellerID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product")
    messages = relationship(
        "ChatMessage",
        back_populates="chat",
        cascade="all, delete-orphan",
    )


class ChatMessage(Base):
    __tablename__ = "ChatMessage"

    MessageID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ChatID = Column(Integer, ForeignKey("Chat.ChatID", ondelete="CASCADE"), nullable=False)
    SenderID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    Message = Column(Text, nullable=False)
    IsRead = Column(Boolean, default=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
