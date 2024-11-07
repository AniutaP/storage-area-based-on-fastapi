from fastapi import Depends, HTTPException
from typing import AsyncGenerator
from jose import JWTError, jwt

from src.database.models import UserModel
from src.schemas.tokens import oauth2_scheme
from src.repositories.login import LoginRepository
from src.repositories.products import ProductRepository
from src.repositories.users import UserRepository
from src.services.products import ProductService
from src.repositories.orders import OrderRepository
from src.services.orders import OrderService
from src.services.login import LoginService
from src.services.users import UserService
from src.core.settings import database, configs
from src.middlewares import HTTPErrorCodes


async def get_db_session() -> AsyncGenerator:
    async with database.session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


user_repository = UserRepository()
user_service = UserService(user_repository)


def get_user_service() -> UserService:
    return user_service


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service = Depends(get_user_service),
        db_session = Depends(get_db_session)
) -> UserModel:

    message = "Could not validate credentials"
    error = HTTPErrorCodes(401, message)
    credentials_exception =  HTTPException(error.code, error.message)

    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user: UserModel = await user_service.get_by_email(email=username, db_session=db_session)
    if user is None:
        raise credentials_exception
    return user


product_repository = ProductRepository()
product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
    return product_service


order_repository = OrderRepository()
order_service = OrderService(order_repository)


def get_order_service() -> OrderService:
    return order_service


login_repository = LoginRepository()
login_service = LoginService(login_repository)


def get_auth_service() -> LoginService:
    return login_service
