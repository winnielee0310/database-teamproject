from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=1)


class UserLogin(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    Account: str
    Password: str
    Email: str


class UserResponse(BaseModel):
    UserID: int
    Account: str
    Email: str
    SellerReputation: float
    BuyerReputation: float

    class Config:
        from_attributes = True


class MemberResponse(BaseModel):
    MemberID: int
    GroupID: int
    MemberName: str

    class Config:
        from_attributes = True


class GroupResponse(BaseModel):
    GroupID: int
    GroupName: str
    Company: Optional[str] = None

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    SellerID: int
    Price: float = Field(..., gt=0)
    ProductName: str = Field(..., min_length=1, max_length=100)
    Description: Optional[str] = None
    Condition: str = Field(..., min_length=1, max_length=50)
    TradeMethod: str = Field(..., min_length=1, max_length=50)
    MemberIDs: List[int] = Field(default_factory=list)
    CustomGroupName: Optional[str] = None
    CustomMemberNames: List[str] = Field(default_factory=list)
    ImageUrl: Optional[str] = None


class ProductResponse(BaseModel):
    ProductID: int
    SellerID: int
    Price: float
    ProductName: str
    Description: Optional[str] = None
    Condition: str
    TradeMethod: str
    Status: str
    ImageUrl: Optional[str] = None
    MemberNames: List[str] = Field(default_factory=list)
    GroupNames: List[str] = Field(default_factory=list)


class WishlistCreate(BaseModel):
    UserID: int
    MemberID: Optional[int] = None
    MaxPrice: float = Field(..., gt=0)
    ConditionReq: Optional[str] = None
    CustomGroupName: Optional[str] = None
    CustomMemberName: Optional[str] = None


class WishlistResponse(BaseModel):
    WishID: int
    UserID: int
    MemberID: int
    MaxPrice: float
    ConditionReq: Optional[str] = None

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    BuyerID: int
    ProductID: int


class OrderResponse(BaseModel):
    OrderID: int
    BuyerID: int
    ProductID: int
    OrderPrice: float
    Status: str
    OrderDate: datetime

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    OrderID: int
    PackingScore: int = Field(..., ge=1, le=5)
    VideoScore: int = Field(..., ge=1, le=5)
    SpeedScore: int = Field(..., ge=1, le=5)
    Comment: Optional[str] = None


class ReviewResponse(BaseModel):
    ReviewID: int
    OrderID: int
    PackingScore: int
    VideoScore: int
    SpeedScore: int
    Comment: Optional[str] = None

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    ProductID: int
    SenderID: int
    ReceiverID: int
    Content: str
    MediaUrl: Optional[str] = None


class MessageResponse(BaseModel):
    MessageID: int
    ProductID: int
    SenderID: int
    ReceiverID: int
    Content: str
    SentAt: datetime
    MediaUrl: Optional[str] = None

    class Config:
        from_attributes = True


class ChatCreate(BaseModel):
    product_id: int
    buyer_id: int
    seller_id: int


class ChatResponse(BaseModel):
    chat_id: int


class ChatMessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    sender_id: int
    message: str
    created_at: datetime
    is_read: bool


class ChatListResponse(BaseModel):
    chat_id: int
    product_name: str
    last_message: str
    updated_at: datetime
    unread_count: int
