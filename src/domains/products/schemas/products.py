from pydantic import BaseModel, ConfigDict, Field


class ProductAddSchema(BaseModel):
    name: str
    description: str | None = Field(default=None)
    price: int = Field(ge=0)
    quantity: int = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)


class ProductSchema(ProductAddSchema):
    id: int


class ProductIdSchema(BaseModel):
    id: int


class ProductUpdateSchema(BaseModel):
    id: int
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)

    model_config = ConfigDict(from_attributes=True)


class DeleteSchema(BaseModel):
    status_process: str = "Product successfully deleted"

    model_config = ConfigDict(from_attributes=True)
