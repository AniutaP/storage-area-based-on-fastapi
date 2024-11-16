from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductDTO:
    name: str | None
    price: Decimal | None
    quantity: int | None
    id: int | None = None
    description: str | None = None
