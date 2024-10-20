from storage_area.repositories.products import ProductRepository
from dataclasses import dataclass


@dataclass
class ProductService:
    repository: ProductRepository

    async def create_product(self, data):
        return await self.repository.create_product(data)

    async def get_all_products(self):
        return await self.repository.get_all_products()

    async def get_product_by_id(self, id):
        return await self.repository.get_product_by_id(id)

    async def update_product_by_id(self, id, data):
        return await self.repository.update_product_by_id(id, data)

    async def delete_product_by_id(self, id):
        return await self.repository.delete_product_by_id(id)
