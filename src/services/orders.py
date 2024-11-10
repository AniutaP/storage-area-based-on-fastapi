from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.products import ProductDTO
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
                raise HTTPException(422, message)
        return True

    async def update_quantity_product(self, order: OrderDTO, db_session: AsyncSession) -> bool:
        from src.depends.products import product_service

        orderitems = order.orderitems
        for orderitem in orderitems:
            product_model = await product_service.get_by_id(orderitem.product_id, db_session)
            new_quantity = product_model.quantity - orderitem.quantity
            product_to_update = ProductDTO(quantity=new_quantity)
            await product_service.update_by_id(orderitem.product_id, product_to_update, db_session)

    async def create(self, order: OrderDTO, db_session: AsyncSession):
        check = await self.check_quantity_product(order, db_session)
        if check:
            await self.update_quantity_product(order, db_session)
            return await self.repository.create(order, db_session)

    async def get_all(self, db_session: AsyncSession):
        return await self.repository.get_all(db_session)

    async def get_by_id(self, id: str, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'Object with id {id} not found'
            raise HTTPException(404, message)
        return result

    async def update_status_by_id(self, id: str, order: OrderDTO, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.update_status_by_id(id, order, db_session)
