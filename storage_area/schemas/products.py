from pydantic import BaseModel, ConfigDict


class SProductAdd(BaseModel):
   name: str
   description: str | None = None
   price: int
   quantity: int

   model_config = ConfigDict(from_attributes=True)


class SProduct(SProductAdd):
   id: int

   model_config = ConfigDict(from_attributes=True)


class SProductUpdate(BaseModel):
   name: str | None = None
   description: str | None = None
   price: int | None = None
   quantity: int | None = None

   model_config = ConfigDict(from_attributes=True)
