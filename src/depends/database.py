from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from src.core.settings import database
from src.core.settings import hawk


async def get_db_session() -> AsyncGenerator:
    async with database.session_factory() as session:
        try:
            yield session

        except IntegrityError:
            await session.rollback()
            message = 'IntegrityError occurred'
            hawk.send(HTTPException(422, message))
            raise HTTPException(422, message)
        except Exception:
            hawk.send(Exception("error description"), {"params": "value"})
            await session.rollback()
            raise
        finally:
            await session.close()
