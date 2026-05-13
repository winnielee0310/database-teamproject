from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    SellerID: int
    Price: float = Field(..., gt=0)
    Condition: str
    TradeMethod: str
    MemberIDs: List[int] # 支援多個成員標記 (雙人卡等)

class ProductResponse(BaseModel):
    ProductID: int
    SellerID: int
    Price: float
    Condition: str
    TradeMethod: str
    Status: str
    class Config:
        from_attributes = True

class WishlistCreate(BaseModel):
    UserID: int
    MemberID: int
    MaxPrice: float = Field(..., gt=0)
    ConditionReq: Optional[str] = None

class OrderCreate(BaseModel):
    BuyerID: int
    ProductID: int
