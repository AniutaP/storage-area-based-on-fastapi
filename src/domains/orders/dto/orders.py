from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OrderItemDTO:
    id: int | None = None
    quantity: int | None = None
    order_id: int | None = None
    product_id: int | None = None


@dataclass
class OrderDTO:
    status: str
    id: int | None = None
    user_id: int | None = None
    created_at: datetime | None = None
    orderitems: list[OrderItemDTO] = field(default_factory=list)


@dataclass
class OrderUpdateDTO:
    status: str
    id: int | None = None
