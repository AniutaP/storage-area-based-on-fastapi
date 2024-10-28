from dataclasses import dataclass, field, asdict


@dataclass
class OrderItemDTO:
    id: int | None = None
    quantity: int | None = None
    order_id: int | None = None
    product_id: int | None = None


@dataclass
class OrderDTO:
    id: int
    status: str
