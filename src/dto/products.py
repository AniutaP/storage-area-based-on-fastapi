from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductDTO:
    id: int | None = None
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity: int | None = None
