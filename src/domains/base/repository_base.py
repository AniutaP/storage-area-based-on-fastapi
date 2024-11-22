from dataclasses import asdict
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar

from src.utils.db_utils import model_to_dict


DTO = TypeVar('DTO')


class BaseRepository:

    def __init__(self, SQLModel, DTO):
        self.SQLModel = SQLModel
        self.DTO = DTO

    async def create(self, model_dto: DTO, db_session: AsyncSession) -> DTO:
        result = self.SQLModel(**asdict(model_dto))
        db_session.add(result)
        await db_session.flush()
        await db_session.commit()
        return self.DTO(**model_to_dict(result))

    async def get_all(self, db_session: AsyncSession) -> list[DTO]:
        query = select(self.SQLModel)
        result = await db_session.scalars(query)
        if not result:
            return []
        models_to_dto = [
            self.DTO(**model_to_dict(model_dto)) for model_dto in result.all()
        ]
        return models_to_dto

    async def get_by_id(self, id: int, db_session: AsyncSession) -> DTO | None:
        result = await db_session.get(self.SQLModel, id)
        if not result:
            return None
        return self.DTO(**model_to_dict(result))

    async def update_by_id(
            self, model_dto: DTO, db_session: AsyncSession
    ) -> DTO | None:
        to_dict = asdict(model_dto)
        query = update(
            self.SQLModel
        ).where(
            self.SQLModel.id == model_dto.id  # type: ignore
        ).values(**to_dict)
        await db_session.execute(query)
        await db_session.commit()
        return model_dto

    async def delete_by_id(self, model_dto: DTO, db_session: AsyncSession) -> None:
        query = delete(
            self.SQLModel
        ).where(self.SQLModel.id == model_dto.id)  # type: ignore
        await db_session.execute(query)
        await db_session.commit()
