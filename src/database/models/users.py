from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models.sqlalchemy_base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    orders = relationship("OrderModel")
