from src.repositories.orders import OrderRepository
from dataclasses import dataclass
from fastapi import HTTPException
from src.middlewares import HttpErrorCodes
from collections import defaultdict


@dataclass
class OrderService:
    repository: OrderRepository

    async def check_quantity_product(self, data: dict) -> bool:
        from src.depends.depends import product_service

        orderitems = data["orderitems"]
        for orderitem in orderitems:
            product_id, quantity = orderitem["product_id"], orderitem["quantity"]
            product_model = await product_service.get_by_id(product_id)
            quantity_product_in_db = product_model.quantity
            if quantity > quantity_product_in_db:
                message = f'Quantity product with id: {product_id} exceeds stock availability'
                error = HttpErrorCodes(422, message)
                raise HTTPException(error.code, error.message)
        return True

    async def create(self, data: dict):
        check = await self.check_quantity_product(data)
        if check:
            return await self.repository.create(data)

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, id: str):
        result = await self.repository.get_by_id(id)
        if result is None:
            message = f'Object with id {id} not found'
            error = HttpErrorCodes(404, message)
            raise HTTPException(error.code, error.message)
        return result

    async def update_by_id(self, id: str, data: dict):
        await self.get_by_id(id)
        return await self.repository.update_by_id(id, data)
