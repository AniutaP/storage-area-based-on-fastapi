from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.core.settings import database


async def get_db_session() -> AsyncGenerator:
    async with database.session_factory() as session:
        try:
            yield session

        except IntegrityError as e:
            await session.rollback()
            message = e.args[0]
            raise HTTPException(422, message)
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
