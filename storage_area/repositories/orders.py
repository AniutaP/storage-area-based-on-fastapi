from storage_area.database.models.models import OrderModel, OrderItemModel, ProductModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class OrderRepository:

    def __init__(self, db_session):
        self._session = db_session

    async def create(self, data) -> OrderModel:
        async with self._session() as session:
            status = data["status"]
            orderitems = data["orderitems"]
            new_order = OrderModel(status=status)
            session.add(new_order)
            await session.flush()
            order_id = new_order.id
            query_insert_item_to_new_order = [
                OrderItemModel(
                    quantity=orderitem["quantity"],
                    order_id=order_id,
                    product_id=orderitem["product_id"],
                )
                for orderitem in orderitems
            ]
            session.add_all(query_insert_item_to_new_order)
            await session.flush()
            query_get_current_order_with_items = select(OrderModel).where(
                OrderModel.id == order_id
            )
            order = await session.scalar(
                query_get_current_order_with_items.options(
                    selectinload(OrderModel.orderitems)
                )
            )
            await session.commit()
            return order

    async def get_all(self) -> list[OrderModel]:
        async with self._session() as session:
            query = select(OrderModel)
            result = await session.scalars(
                query.options(selectinload(OrderModel.orderitems))
            )
            orders = result.all()
            return orders

    async def get_by_id(self, id: str) -> OrderModel | None:
        async with self._session() as session:
            query = select(OrderModel).where(OrderModel.id == int(id))
            order = await session.scalar(
                query.options(selectinload(OrderModel.orderitems))
            )
            return order

    async def update_by_id(self, id: str, data: dict) -> OrderModel:
        async with self._session() as session:
            data = {**data}
            order_to_update = await session.get(OrderModel, int(id))
            for field, value in data.items():
                if value:
                    setattr(order_to_update, field, data[field])
            session.add(order_to_update)
            await session.commit()
            await session.refresh(order_to_update)
            return order_to_update
