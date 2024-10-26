from src.repositories.products import ProductRepository
from dataclasses import dataclass
from fastapi import HTTPException
from src.middlewares import HTTPErrorCodes


@dataclass
class ProductService:
    repository: ProductRepository

    async def create(self, data: dict):
        return await self.repository.create(data)

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, id: str):
        result = await self.repository.get_by_id(id)
        if result is None:
            message = f'Object with id {id} not found'
            error = HTTPErrorCodes(404, message)
            raise HTTPException(error.code, error.message)
        return result

    async def update_by_id(self, id: str, data: dict):
        await self.get_by_id(id)
        return await self.repository.update_by_id(id, data)

    async def delete_by_id(self, id: str):
        await self.get_by_id(id)
        return await self.repository.delete_by_id(id)
