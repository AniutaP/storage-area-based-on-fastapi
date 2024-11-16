from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.configs.settings import database
from src.configs.settings import hawk


async def get_db_session() -> AsyncGenerator:
    async with database.session_factory() as session:
        try:
            yield session

        except IntegrityError:
            await session.rollback()
            message = 'IntegrityError occurred'
            hawk.send(HTTPException(422, message))
            raise HTTPException(422, message)

        finally:
            await session.close()
