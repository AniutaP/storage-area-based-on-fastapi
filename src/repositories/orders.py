from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.orders import OrderModel, OrderItemModel

from src.dto.orders import OrderDTO, OrderItemDTO
from src.utils import model_to_dict


class OrderRepository:

    async def create(self, order: OrderDTO, db_session: AsyncSession) -> OrderDTO:
            status = order.status
            orderitems = order.orderitems
            new_order = OrderModel(status=status)
            db_session.add(new_order)
            await db_session.flush()
            order_id = new_order.id
            query_insert_item_to_new_order = (
                OrderItemModel(
                    quantity=orderitem.quantity,
                    order_id=order_id,
                    product_id=orderitem.product_id,
                )
                for orderitem in orderitems
            )
            db_session.add_all(query_insert_item_to_new_order)
            await db_session.flush()
            query_get_current_order_with_items = select(OrderModel).where(
                OrderModel.id == order_id
            )
            result_order = await db_session.scalar(
                query_get_current_order_with_items.options(
                    selectinload(OrderModel.orderitems)
                )
            )
            await db_session.commit()
            order = OrderDTO(**model_to_dict(result_order))
            order.orderitems = [OrderItemDTO(**model_to_dict(item)) for item in result_order.orderitems]
            return order

    async def get_all(self, db_session: AsyncSession) -> list[OrderDTO]:
            query = select(OrderModel)
            result = await db_session.scalars(
                query.options(selectinload(OrderModel.orderitems))
            )
            if not result:
                return []

            orders = []
            for result_order in result.all():
                order = OrderDTO(**model_to_dict(result_order))
                order.orderitems = [OrderItemDTO(**model_to_dict(item)) for item in result_order.orderitems]
                orders.append(order)

            return orders

    async def get_by_id(self, id: str, db_session: AsyncSession) -> OrderDTO | None:
            query = select(OrderModel).where(OrderModel.id == int(id))
            result = await db_session.scalar(
                query.options(selectinload(OrderModel.orderitems))
            )
            if not result:
                return None

            order = OrderDTO(**model_to_dict(result))
            order.orderitems = [OrderItemDTO(**model_to_dict(item)) for item in result.orderitems]
            return order

    async def update_status_by_id(self, id: str, order: OrderDTO, db_session: AsyncSession) -> OrderDTO:
            order_new_status = order.status
            order_to_update = await db_session.get(OrderModel, int(id))
            if order_new_status:
                setattr(order_to_update, 'status', order_new_status)
            db_session.add(order_to_update)
            await db_session.commit()
            await db_session.refresh(order_to_update)
            return OrderDTO(**model_to_dict(order_to_update))
