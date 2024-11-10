from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import Hasher
from src.dto.users import UserDTO
from src.repositories.users import UserRepository


class LoginService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def authenticate_user(
            self, email: str, password: str, db_session: AsyncSession
    ) -> UserDTO | None:

        user = await self.repository.get_by_email(email=email, db_session=db_session)

        if not user:
            return None

        if not Hasher.verify_password(password, user.password):
            return None

        return user
