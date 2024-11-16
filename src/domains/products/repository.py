from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.base.repository_base import BaseRepository
from src.core.database.models.products import ProductModel
from src.domains.products.dto.products import ProductDTO
from src.utils.db_utils import model_to_dict


class ProductRepository(BaseRepository):

    def __init__(self):
        super().__init__(ProductModel, ProductDTO)

    async def get_by_name(self, name: str, db_session: AsyncSession) -> ProductDTO | None:
        query = select(ProductModel).where(ProductModel.name == name)
        product = await db_session.scalar(query)
        if not product:
            return None
        return ProductDTO(**model_to_dict(product))
