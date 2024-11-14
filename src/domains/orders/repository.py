from sqlalchemy import select, desc, func, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database.models.orders import OrderModel, OrderItemModel
from src.core.database.models.products import ProductModel
from src.domains.orders.dto.orders import OrderDTO, OrderItemDTO
from src.utils.db_utils import model_to_dict


class OrderRepository:

    async def create(self, order: OrderDTO, db_session: AsyncSession) -> OrderDTO:
        status, user_id, orderitems = order.status, order.user_id, order.orderitems
        new_order = OrderModel(status=status, user_id=user_id)
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

        order_to_dto = OrderDTO(**model_to_dict(result_order))
        order_to_dto.orderitems = [
            OrderItemDTO(**model_to_dict(item)) for item in result_order.orderitems
        ]
        await db_session.commit()
        return order_to_dto

    async def get_all(
            self, db_session: AsyncSession, user_id: int | None = None
    ) -> list[OrderDTO]:
        if user_id:
            query = select(OrderModel).where(OrderModel.user_id == user_id)
        else:
            query = select(OrderModel)

        result = await db_session.execute(
            query.options(
                joinedload(OrderModel.orderitems)
            ).order_by(desc(OrderModel.created_at))
        )
        query_result = result.unique().scalars().all()
        if not query_result:
            return []

        orders_to_dto = []
        for order in query_result:
            order_to_dto = OrderDTO(**model_to_dict(order))
            order_to_dto.orderitems = [
                OrderItemDTO(**model_to_dict(item)) for item in order.orderitems
            ]
            orders_to_dto.append(order_to_dto)

        return orders_to_dto

    async def get_by_id(
            self, id: int, db_session: AsyncSession
    ) -> OrderDTO | None:
        query = select(OrderModel).where(OrderModel.id == id).options(
            joinedload(OrderModel.orderitems)
        )
        result = await db_session.scalar(query)
        if not result:
            return None

        order_to_dto = OrderDTO(**model_to_dict(result))
        order_to_dto.orderitems = [
            OrderItemDTO(**model_to_dict(item)) for item in result.orderitems
        ]
        return order_to_dto

    async def get_total_order_sum_by_user_id(
            self, user_id: int, db_session: AsyncSession
    ) -> dict:
        query = select(
            OrderModel.user_id, func.sum(
                OrderItemModel.quantity * ProductModel.price
            ).label('total')
        ).where(
            OrderModel.user_id == user_id
        ).join(
            OrderItemModel, and_(OrderModel.id == OrderItemModel.order_id)
        ).join(
            ProductModel, and_(OrderItemModel.product_id == ProductModel.id)
        ).group_by(OrderModel.user_id)

        result = await db_session.execute(query)
        total = result.one_or_none()[1]
        data = {'id': user_id, 'total': total}
        return data

    async def update_status_by_id(
            self, order: OrderDTO, db_session: AsyncSession
    ) -> OrderDTO:
        order_new_status = order.status
        order_to_update = await db_session.get(OrderModel, order.id)
        if order_new_status:
            setattr(order_to_update, 'status', order_new_status)
        db_session.add(order_to_update)
        order_to_dto = OrderDTO(**model_to_dict(order_to_update))
        await db_session.commit()
        await db_session.refresh(order_to_update)
        return order_to_dto
