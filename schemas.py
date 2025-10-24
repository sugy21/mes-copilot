from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


# Base schemas
class OrderBase(BaseModel):
    """Base schema for Order data"""

    order_name: str = Field(min_length=1, max_length=100)
    product_code: str = Field(min_length=1, max_length=50)


class WorkResultBase(BaseModel):
    """Base schema for WorkResult data"""

    order_id: int = Field(gt=0)
    status: str = Field(min_length=1, max_length=50)
    worker: Optional[str] = None
    inspector: Optional[str] = None


# Create schemas
class OrderCreate(OrderBase):
    """Schema for order creation"""

    model_config = ConfigDict(extra="forbid")


class WorkResultCreate(WorkResultBase):
    """Schema for work result creation"""

    model_config = ConfigDict(extra="forbid")


# Update schemas
class OrderUpdate(BaseModel):
    """Schema for order updates"""

    order_name: Optional[str] = Field(None, min_length=1, max_length=100)
    product_code: Optional[str] = Field(None, min_length=1, max_length=50)

    model_config = ConfigDict(extra="forbid")


class WorkResultUpdate(BaseModel):
    """Schema for work result updates"""

    status: Optional[str] = Field(None, min_length=1, max_length=50)
    worker: Optional[str] = None
    inspector: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


# Response schemas
class OrderResponse(OrderBase):
    """Schema for order responses"""

    id: int = Field(gt=0)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkResultResponse(WorkResultBase):
    """Schema for work result responses"""

    id: int = Field(gt=0)
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


# Relationship schemas
class OrderWithResults(OrderResponse):
    """Extended order response with work results"""

    results: List[WorkResultResponse] = Field(default_factory=list)


class WorkResultWithOrder(WorkResultResponse):
    """Extended work result response with order"""

    order: OrderResponse
