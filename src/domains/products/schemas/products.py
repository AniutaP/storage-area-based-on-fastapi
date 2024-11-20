from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


class ProductAddSchema(BaseModel):
    name: str
    description: str | None = Field(default=None, max_length=150)
    price: Decimal = Field(ge=0)
    quantity: int = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(ProductAddSchema):
    id: int


class ProductIdSchema(BaseModel):
    id: int


class DeleteSchema(BaseModel):
    status_process: str = "Product successfully deleted"

    model_config = ConfigDict(from_attributes=True)
