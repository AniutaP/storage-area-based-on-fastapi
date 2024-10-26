from pydantic import BaseModel, ConfigDict, field_validator
from fastapi import HTTPException
from src.middlewares import HTTPErrorCodes


class ProductAddSchema(BaseModel):
    name: str
    description: str | None = None
    price: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("price")
    def check_price(cls, value):
        if value < 0:
            message = 'Price should not be negative'
            error = HTTPErrorCodes(422, message)
            raise HTTPException(error.code, error.message)
        return value

    @field_validator("quantity")
    def check_quantity(cls, value):
        if value < 0:
            message = 'Quantity should not be negative'
            error = HTTPErrorCodes(422, message)
            raise HTTPException(error.code, error.message)
        return value


class ProductSchema(ProductAddSchema):
    id: int


class ProductUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("price")
    def check_price(cls, value):
        if not value or value > 0:
            return value
        message = 'Price should not be negative'
        error = HTTPErrorCodes(422, message)
        raise HTTPException(error.code, error.message)

    @field_validator("quantity")
    def check_quantity(cls, value):
        if not value or value > 0:
            return value
        message = 'Quantity should not be negative'
        error = HTTPErrorCodes(422, message)
        raise HTTPException(error.code, error.message)


