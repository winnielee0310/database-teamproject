from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- User ---
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

# --- Group & Member ---
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

# --- Product ---
class ProductCreate(BaseModel):
    SellerID: int
    Price: float = Field(..., gt=0)
    Condition: str
    TradeMethod: str
    MemberIDs: List[int]

class ProductResponse(BaseModel):
    ProductID: int
    SellerID: int
    Price: float
    Condition: str
    TradeMethod: str
    Status: str
    class Config:
        from_attributes = True

# --- Wishlist ---
class WishlistCreate(BaseModel):
    UserID: int
    MemberID: int
    MaxPrice: float = Field(..., gt=0)
    ConditionReq: Optional[str] = None

class WishlistResponse(BaseModel):
    WishID: int
    UserID: int
    MemberID: int
    MaxPrice: float
    ConditionReq: Optional[str]
    class Config:
        from_attributes = True

# --- Order ---
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

# --- Review ---
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
    Comment: Optional[str]
    class Config:
        from_attributes = True
