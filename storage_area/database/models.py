from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, func, ForeignKey
from datetime import datetime
from storage_area.database.database import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    price: Mapped[int] = mapped_column(Numeric(precision=10, scale=2))
    quantity: Mapped[int]
#    orderitems = relationship("OrderItemOrm")


class OrderModel(BaseModel):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[str]
#    orderitems = relationship("OrderItemOrm")


class OrderItemModel(BaseModel):
    __tablename__ = "orderitems"
    id: Mapped[int] = mapped_column(primary_key=True)
#    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
#    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int]


