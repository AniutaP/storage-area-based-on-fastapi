from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, UniqueConstraint
from datetime import datetime
from src.database.models.sqlalchemy_base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = "orders"

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[str]
    orderitems = relationship("OrderItemModel")


class OrderItemModel(BaseModel):
    __tablename__ = "orderitems"
    __table_args__ = (UniqueConstraint('order_id', 'product_id'),)

    quantity: Mapped[int]
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
