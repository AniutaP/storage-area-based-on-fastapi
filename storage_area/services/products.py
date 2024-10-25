from storage_area.repositories.products import ProductRepository
from dataclasses import dataclass
from fastapi import HTTPException
from storage_area.middlewares import HTTP_ERROR_CODES


@dataclass
class ProductService:
    repository: ProductRepository

    async def create(self, data):
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

    async def delete_by_id(self, id):
        await self.get_by_id(id)
        return await self.repository.delete_by_id(id)
