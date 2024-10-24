from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, func, ForeignKey
from datetime import datetime
from storage_area.database.models.sqlalchemy_base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(Numeric(precision=10, scale=2))
    quantity: Mapped[int]


class OrderModel(BaseModel):
    __tablename__ = "orders"

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[str]
    orderitems = relationship("OrderItemModel")


class OrderItemModel(BaseModel):
    __tablename__ = "orderitems"

    quantity: Mapped[int]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
