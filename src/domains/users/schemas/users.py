from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List

from src.domains.orders.schemas.orders import OrderSchema


class UserAddSchema(BaseModel):
    name: str | None = Field(default=None)
    email: EmailStr
    password: str = Field(min_length=5)

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    id: int
    name: str | None = Field(default=None)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserIdSchema(BaseModel):
    id: int


class UserUpdateSchema(UserSchema):
    password: str = Field(min_length=5)


class UserIdTotalSchema(UserIdSchema):
    total: Decimal | None = Field(default=None)


class UserWithOrdersSchema(UserSchema):
    orders: List[OrderSchema]


class DeleteSchema(BaseModel):
    status_process: str = "User successfully deleted"

    model_config = ConfigDict(from_attributes=True)
