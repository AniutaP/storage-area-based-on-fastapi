from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, UniqueConstraint, CheckConstraint
from src.core.database.models.sqlalchemy_base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = 'products'
    __table_args__ = (
        UniqueConstraint('name'),
        CheckConstraint('quantity >= 0', name='check_not_neg'),
    )

    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(Numeric(precision=10, scale=2))
    quantity: Mapped[int]
