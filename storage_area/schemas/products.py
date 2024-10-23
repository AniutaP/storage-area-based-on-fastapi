from pydantic import BaseModel, ConfigDict, field_validator


class SProductAdd(BaseModel):
   name: str
   description: str | None = None
   price: int
   quantity: int

   model_config = ConfigDict(from_attributes=True)

   @field_validator('price')
   def check_price(cls, value):
      if value < 0:
         raise ValueError('Price should not be negative')
      return value

   @field_validator('quantity')
   def check_quantity(cls, value):
      if value < 0:
         raise ValueError('Quantity should not be negative')
      return value


class SProduct(SProductAdd):
   id: int


class SProductUpdate(BaseModel):
   name: str | None = None
   description: str | None = None
   price: int | None = None
   quantity: int | None = None

   model_config = ConfigDict(from_attributes=True)

   @field_validator('price')
   def check_price(cls, value):
      if not value or value > 0:
         return value
      raise ValueError('Price should not be negative')


   @field_validator('quantity')
   def check_quantity(cls, value):
      if not value or value > 0:
         return value
      raise ValueError('Quantity should not be negative')
