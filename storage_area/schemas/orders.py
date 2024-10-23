from pydantic import BaseModel, ConfigDict, field_validator
from typing import List


class SOrderItem(BaseModel):
    quantity: int
    product_id: int

    @field_validator('quantity')
    def check_quantity(cls, value):
        if value < 0:
            raise ValueError('Quantity should not be negative')
        return value

    model_config = ConfigDict(from_attributes=True)


class SOrderAdd(BaseModel):
    status: str
    orderitems: List[SOrderItem]

    model_config = ConfigDict(from_attributes=True)


class SOrder(SOrderAdd):
    id: int


class SOrderStatusUpdate(BaseModel):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
