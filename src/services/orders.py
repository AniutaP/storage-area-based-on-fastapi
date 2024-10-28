from src.repositories.orders import OrderRepository
from dataclasses import dataclass
from fastapi import HTTPException
from src.middlewares import HTTPErrorCodes
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class OrderService:
    repository: OrderRepository

    async def check_quantity_product(self, data: dict, db_session: AsyncSession) -> bool:
        from src.depends.depends import product_service

        orderitems = data["orderitems"]
        for orderitem in orderitems:
            product_id, quantity = orderitem["product_id"], orderitem["quantity"]
            product_model = await product_service.get_by_id(product_id, db_session)
            quantity_product_in_db = product_model.quantity
            if quantity > quantity_product_in_db:
                message = f'Quantity product with id: {product_id} exceeds stock availability'
                error = HTTPErrorCodes(422, message)
                raise HTTPException(error.code, error.message)
        return True

    async def create(self, data: dict, db_session: AsyncSession):
        check = await self.check_quantity_product(data, db_session)
        if check:
            return await self.repository.create(data, db_session)

    async def get_all(self, db_session: AsyncSession):
        return await self.repository.get_all(db_session)

    async def get_by_id(self, id: str, db_session: AsyncSession):
        result = await self.repository.get_by_id(id, db_session)
        if result is None:
            message = f'Object with id {id} not found'
            error = HTTPErrorCodes(404, message)
            raise HTTPException(error.code, error.message)
        return result

    async def update_by_id(self, id: str, data: dict, db_session: AsyncSession):
        await self.get_by_id(id, db_session)
        return await self.repository.update_by_id(id, data, db_session)
