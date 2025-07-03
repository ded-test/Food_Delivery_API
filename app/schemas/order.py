from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

from app.schemas.user import UserResponse


class OrderStatus(str, Enum):
    NEW = "new"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    CANCELED = "canceled"

# Схемы для элементов заказа
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, default=1)
    price_per_item: float = Field(ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = Field(None, ge=1)
    price_per_item: Optional[float] = Field(None, ge=0)


class OrderItemResponse(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int

# Схемы для заказов
class OrderBase(BaseModel):
    delivery_address: str = Field(min_length=1, max_length=255)


class OrderCreate(OrderBase):
    user_id: int
    items: List[OrderItemCreate] = Field(min_length=1)


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = Field(None, min_length=1, max_length=255)
    items: Optional[List[OrderItemCreate]] = None


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse] = []

# Расширенная схема ответа с информацией о пользователе
class OrderWithUserResponse(OrderResponse):
    model_config = ConfigDict(from_attributes=True)
    user: Optional[UserResponse] = None


# Для пагинированного списка заказов с метаданными
class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    size: int

# Cпециализированные схемы для работы со статусами заказов
class OrderStatusUpdate(BaseModel):
    status: OrderStatus

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if not isinstance(v, OrderStatus):
            try:
                # Попытка создать OrderStatus из строки
                return OrderStatus(v)
            except ValueError:
                raise ValueError(f'Invalid order status: {v}. Must be one of: {[s.value for s in OrderStatus]}')
        return v


class OrderStatusSchema(BaseModel):
    status: OrderStatus