from pydantic import BaseModel, ConfigDict


class SProductAdd(BaseModel):
   model_config = ConfigDict(from_attributes=True)
   name: str
   description: str | None = None
   price: int
   quantity: int


class SProduct(SProductAdd):
   model_config = ConfigDict(from_attributes=True)
   id: int


class SProductId(BaseModel):
   model_config = ConfigDict(from_attributes=True)
   id: int


class SProductUpdate(BaseModel):
   model_config = ConfigDict(from_attributes=True)
   name: str | None = None
   description: str | None = None
   price: int | None = None
   quantity: int | None = None