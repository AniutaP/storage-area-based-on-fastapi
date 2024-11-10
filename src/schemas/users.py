from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List

from src.schemas.orders import OrderSchema


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


class UserUpdateSchema(BaseModel):
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    password: int | None = Field(default=None, min_length=5)

    model_config = ConfigDict(from_attributes=True)


class UserWithOrdersSchema(UserSchema):
    orders: List[OrderSchema]
