from dataclasses import asdict
from src.database.models.orders_models import OrderModel, OrderItemModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.dto.orders import OrderDTO


class OrderRepository:

    async def create(self, data: OrderDTO, db_session: AsyncSession) -> OrderModel:
            order_data = asdict(data)
            status = order_data["status"]
            orderitems = order_data["orderitems"]
            new_order = OrderModel(status=status)
            db_session.add(new_order)
            await db_session.flush()
            order_id = new_order.id
            query_insert_item_to_new_order = (
                OrderItemModel(
                    quantity=orderitem["quantity"],
                    order_id=order_id,
                    product_id=orderitem["product_id"],
                )
                for orderitem in orderitems
            )
            db_session.add_all(query_insert_item_to_new_order)
            await db_session.flush()
            query_get_current_order_with_items = select(OrderModel).where(
                OrderModel.id == order_id
            )
            order = await db_session.scalar(
                query_get_current_order_with_items.options(
                    selectinload(OrderModel.orderitems)
                )
            )
            await db_session.commit()
            return order

    async def get_all(self, db_session: AsyncSession) -> list[OrderModel]:
            query = select(OrderModel)
            result = await db_session.scalars(
                query.options(selectinload(OrderModel.orderitems))
            )
            orders = result.all()
            return orders

    async def get_by_id(self, id: str, db_session: AsyncSession) -> OrderModel | None:
            query = select(OrderModel).where(OrderModel.id == int(id))
            order = await db_session.scalar(
                query.options(selectinload(OrderModel.orderitems))
            )
            return order

    async def update_by_id(self, id: str, data: OrderDTO, db_session: AsyncSession) -> OrderModel:
            order_data = asdict(data)
            order_to_update = await db_session.get(OrderModel, int(id))
            for field, value in order_data.items():
                if value:
                    setattr(order_to_update, field, order_data[field])
            db_session.add(order_to_update)
            await db_session.commit()
            await db_session.refresh(order_to_update)
            return order_to_update
