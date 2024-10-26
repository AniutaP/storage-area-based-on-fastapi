from pydantic import BaseModel, ConfigDict, field_validator
from typing import List
from src.middlewares import HttpErrorCodes
from fastapi import HTTPException


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    def check_quantity(cls, value):
        if value < 0:
            message = 'Quantity should not be negative'
            error = HttpErrorCodes(422, message)
            raise HTTPException(error.code, error.message)
        return value

    model_config = ConfigDict(from_attributes=True)


class OrderAddSchema(BaseModel):
    status: str
    orderitems: List[OrderItemSchema]

    model_config = ConfigDict(from_attributes=True)


class OrderSchema(OrderAddSchema):
    id: int


class OrderStatusUpdateSchema(BaseModel):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
