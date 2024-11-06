from dataclasses import dataclass, field


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
    orderitems: list[OrderItemDTO] = field(default_factory=list)
