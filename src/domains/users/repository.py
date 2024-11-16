from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.base.repository_base import BaseRepository
from src.core.database.models.users import UserModel
from src.domains.users.dto.users import UserDTO
from src.utils.db_utils import model_to_dict


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(UserModel, UserDTO)

    async def get_by_email(self, email: str, db_session: AsyncSession) -> UserDTO | None:
        query = select(UserModel).where(UserModel.email == email)
        user = await db_session.scalar(query)
        if not user:
            return None
        return UserDTO(**model_to_dict(user))
