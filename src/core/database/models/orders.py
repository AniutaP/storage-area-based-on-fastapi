from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, UniqueConstraint
from datetime import datetime
from src.core.database.models.sqlalchemy_base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = 'orders'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    orderitems = relationship('OrderItemModel')


class OrderItemModel(BaseModel):
    __tablename__ = 'orderitems'
    __table_args__ = (
        UniqueConstraint('order_id', 'product_id'),
    )

    quantity: Mapped[int]
    order_id: Mapped[int] = mapped_column(
        ForeignKey('orders.id', ondelete='CASCADE'), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
