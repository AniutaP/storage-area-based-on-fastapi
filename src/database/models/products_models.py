from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric
from src.database.models.sqlalchemy_base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(Numeric(precision=10, scale=2))
    quantity: Mapped[int] = mapped_column(index=True)