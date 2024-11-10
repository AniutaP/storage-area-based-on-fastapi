from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.orders import OrderModel, OrderItemModel
from src.database.models.products import ProductModel
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

            for orderitem in orderitems:
                product_to_update = await db_session.get(ProductModel, orderitem.product_id)
                new_quantity = product_to_update.quantity - orderitem.quantity
                setattr(product_to_update, 'quantity', new_quantity)
                db_session.add(product_to_update)
            await db_session.flush()

            query_get_current_order_with_items = select(OrderModel).where(
                OrderModel.id == order_id
            )
            result_order = await db_session.scalar(
                query_get_current_order_with_items.options(
                    joinedload(OrderModel.orderitems)
                )
            )

            orders_to_dto = OrderDTO(**model_to_dict(result_order))
            orders_to_dto.orderitems = [OrderItemDTO(**model_to_dict(item)) for item in result_order.orderitems]
            await db_session.commit()
            return orders_to_dto

    async def get_all(self, db_session: AsyncSession) -> list[OrderDTO]:
            query = select(OrderModel)
            result = await db_session.scalars(
                query.options(joinedload(OrderModel.orderitems))
            )
            if not result:
                return []

            orders_to_dto = []
            for result_order in result.all():
                order = OrderDTO(**model_to_dict(result_order))
                order.orderitems = [OrderItemDTO(**model_to_dict(item)) for item in result_order.orderitems]
                orders_to_dto.append(order)

            return orders_to_dto

    async def get_by_id(self, id: str, db_session: AsyncSession) -> OrderDTO | None:
            query = select(OrderModel).where(OrderModel.id == int(id))
            result = await db_session.scalar(
                query.options(joinedload(OrderModel.orderitems))
            )
            if not result:
                return None

            order_to_dto = OrderDTO(**model_to_dict(result))
            order_to_dto.orderitems = [OrderItemDTO(**model_to_dict(item)) for item in result.orderitems]
            return order_to_dto

    async def update_status_by_id(self, id: str, order: OrderDTO, db_session: AsyncSession) -> OrderDTO:
            order_new_status = order.status
            order_to_update = await db_session.get(OrderModel, int(id))
            if order_new_status:
                setattr(order_to_update, 'status', order_new_status)
            db_session.add(order_to_update)
            order_to_dto = OrderDTO(**model_to_dict(order_to_update))
            await db_session.commit()
            await db_session.refresh(order_to_update)
            return order_to_dto
