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


class UserIdTotalSchema(UserIdSchema):
    total: Decimal | None = Field(default=None)


class UserWithOrdersSchema(UserSchema):
    orders: List[OrderSchema]


class UserUpdateSchema(BaseModel):
    id: int
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    password: int | None = Field(default=None, min_length=5)

    model_config = ConfigDict(from_attributes=True)


class DeleteSchema(BaseModel):
    status_process: str = "User successfully deleted"

    model_config = ConfigDict(from_attributes=True)
