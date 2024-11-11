from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.core.settings import database


async def get_db_session() -> AsyncGenerator:
    async with database.session_factory() as session:
        try:
            yield session

        except IntegrityError:
            await session.rollback()
            message = 'IntegrityError occurred'
            raise HTTPException(422, message)
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
