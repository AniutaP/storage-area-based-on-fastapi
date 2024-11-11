from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import hawk
from src.repositories.orders import OrderRepository
from src.dto.orders import OrderDTO


class OrderService:

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def check_quantity_product(self, order: OrderDTO, db_session: AsyncSession) -> bool:
        from src.depends.products import product_service

        orderitems = order.orderitems
        for orderitem in orderitems:
            product_model = await product_service.get_by_id(orderitem.product_id, db_session)
            quantity_product_in_db = product_model.quantity
            if orderitem.quantity > quantity_product_in_db:
                message = f'Quantity product with id: {orderitem.product_id} exceeds stock availability'
                hawk.send(HTTPException(422, message))
                raise HTTPException(422, message)
        return True

    async def create(self, order: OrderDTO, db_session: AsyncSession):
        check = await self.check_quantity_product(order, db_session)
        if check:
            return await self.repository.create(order, db_session)

    async def get_all(self, db_session: AsyncSession, user_id: int | None = None):
        return await self.repository.get_all(db_session, user_id)

    async def get_by_id(self, id: int, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'Object with id {id} not found'
            hawk.send(HTTPException(404, message))
            raise HTTPException(404, message)
        return result

    async def update_status_by_id(self, order: OrderDTO, db_session: AsyncSession):
        await self.get_by_id(order.id, db_session)
        return await self.repository.update_status_by_id(order, db_session)
