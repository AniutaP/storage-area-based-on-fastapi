from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.security.tokens.dto.tokens import TokenPayloadDTO
from src.domains.users.dto.users import AdminDTO, UserDTO
from src.domains.users.repository import UserRepository
from src.domains.users.service import UserService
from src.domains.users.dto.admin import configs, admin
from src.depends.database import get_db_session
from src.configs.settings import hawk
from src.security.tokens.service import oauth2_scheme

user_repository = UserRepository()
user_service = UserService(user_repository)


def get_user_service() -> UserService:
    return user_service


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(get_user_service),
        db_session: AsyncSession = Depends(get_db_session)
) -> UserDTO | AdminDTO:

    message = "Could not validate credentials"
    credentials_exception = HTTPException(401, message)

    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
        token_payload_dto = TokenPayloadDTO(**payload)
        email = token_payload_dto.sub
        if email is None:
            raise credentials_exception
    except JWTError:
        hawk.send(JWTError("error description"), {"params": "value"})
        raise credentials_exception

    user = await user_service.get_by_email(email=email, db_session=db_session)
    if user is None:
        raise credentials_exception

    if user.email == admin.email:
        user.is_superuser = True
        return user

    return user
