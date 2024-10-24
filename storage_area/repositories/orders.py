from storage_area.database.models.models import OrderModel, OrderItemModel, ProductModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from collections import defaultdict


class OrderRepository:

    def __init__(self, db_session):
        self._session = db_session

    async def create(self, data) -> OrderModel:
        async with self._session() as session:
            status = data["status"]
            orderitems = data["orderitems"]
            count_quantity_by_product_id = defaultdict(int)
            for orderitem in orderitems:
                product_id, quantity = orderitem["product_id"], orderitem["quantity"]
                count_quantity_by_product_id[product_id] += quantity
            for product_id, quantity in count_quantity_by_product_id.items():
                product_model = await session.get(ProductModel, product_id)
                quantity_product_in_db = product_model.quantity
                if quantity > quantity_product_in_db:
                    raise ValueError(
                        f"Quantity product with id: {product_id} exceeds stock availability"
                    )

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

    async def get_by_id(self, id: int) -> OrderModel | None:
        async with self._session() as session:
            order = await session.get(OrderModel, id)
            if order is None:
                return None
            query = select(OrderModel).where(OrderModel.id == id)
            order = await session.scalar(
                query.options(selectinload(OrderModel.orderitems))
            )
            return order

    async def update_by_id(self, id: int, data: dict) -> OrderModel:
        async with self._session() as session:
            data = {**data}
            order_to_update = await session.get(OrderModel, id)
            for field, value in data.items():
                if value:
                    setattr(order_to_update, field, data[field])
            session.add(order_to_update)
            await session.commit()
            await session.refresh(order_to_update)
            return order_to_update
