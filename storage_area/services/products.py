from storage_area.repositories.products import ProductRepository
from dataclasses import dataclass


@dataclass
class ProductService:
    repository: ProductRepository

    async def create(self, data):
        return await self.repository.create(data)

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, id):
        return await self.repository.get_by_id(id)

    async def update_by_id(self, id, data):
        return await self.repository.update_by_id(id, data)

    async def delete_by_id(self, id):
        return await self.repository.delete_by_id(id)
