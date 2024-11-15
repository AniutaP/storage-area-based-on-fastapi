from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, ForeignKeyConstraint, UniqueConstraint
from datetime import datetime
from src.core.database.models.sqlalchemy_base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    user_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    orderitems = relationship('OrderItemModel')


class OrderItemModel(BaseModel):
    __tablename__ = 'orderitems'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        UniqueConstraint('product_id', 'order_id'),
    )

    quantity: Mapped[int]
    order_id: Mapped[int] = mapped_column(nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
