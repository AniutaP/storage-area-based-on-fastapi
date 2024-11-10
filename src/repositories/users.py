from dataclasses import asdict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import UserModel
from src.dto.users import UserDTO
from src.utils import model_to_dict


class UserRepository:

    async def create(self, user: UserDTO, db_session: AsyncSession) -> UserDTO:
        user_data = asdict(user)
        new_user = UserModel(**user_data)
        db_session.add(new_user)
        await db_session.flush()
        await db_session.commit()
        return UserDTO(**model_to_dict(new_user))

    async def get_all(self, db_session: AsyncSession) -> list[UserDTO]:
        query = select(UserModel)
        result = await db_session.scalars(query)
        if not result:
            return []
        users = [UserDTO(**model_to_dict(user)) for user in result.all()]
        return users

    async def get_by_id(self, id: str, db_session: AsyncSession) -> UserDTO | None:
        user = await db_session.get(UserModel, int(id))
        if not user:
            return None
        return UserDTO(**model_to_dict(user))

    async def get_by_email(self, email: str, db_session: AsyncSession) -> UserDTO | None:
        query = select(UserModel).where(UserModel.email == email)
        user = await db_session.scalar(query)
        if not user:
            return None
        return UserDTO(**model_to_dict(user))

    async def update_by_id(self, id: str, user: UserDTO, db_session: AsyncSession) -> UserDTO | None:
        user_data = asdict(user)
        user_to_update = await db_session.get(UserModel, int(id))
        for field, value in user_data.items():
            if value:
                setattr(user_to_update, field, user_data[field])
        db_session.add(user_to_update)
        await db_session.commit()
        await db_session.refresh(user_to_update)
        return UserDTO(**model_to_dict(user_to_update))

    async def delete_by_id(self, id: str, db_session: AsyncSession) -> None:
        user_to_delete = await db_session.get(UserModel, int(id))
        await db_session.delete(user_to_delete)
        await db_session.commit()
