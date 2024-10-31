from pydantic import BaseModel, ConfigDict, Field
from typing import List
from src.middlewares import HTTPErrorCodes
from fastapi import HTTPException


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(ge=0)

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
