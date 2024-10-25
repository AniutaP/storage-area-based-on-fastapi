from storage_area.repositories.orders import OrderRepository
from dataclasses import dataclass
from fastapi import HTTPException
from storage_area.middlewares import HTTP_ERROR_CODES
from collections import defaultdict


@dataclass
class OrderService:
    repository: OrderRepository

    async def create(self, data):
        from storage_area.depends.depends import product_service

        orderitems = data["orderitems"]
        count_quantity_by_product_id = defaultdict(int)
        for orderitem in orderitems:
            product_id, quantity = orderitem["product_id"], orderitem["quantity"]
            count_quantity_by_product_id[product_id] += quantity
        for product_id, quantity in count_quantity_by_product_id.items():
            product_model = await product_service.get_by_id(product_id)
            quantity_product_in_db = product_model.quantity
            if quantity > quantity_product_in_db:
                raise HTTPException(
                    422,
                    f"Quantity product with id: {product_id} exceeds stock availability"
                )

        return await self.repository.create(data)

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, id):
        result = await self.repository.get_by_id(id)
        if result is None:
            raise HTTPException(404, HTTP_ERROR_CODES[404])
        return result

    async def update_by_id(self, id, data):
        await self.get_by_id(id)
        return await self.repository.update_by_id(id, data)
