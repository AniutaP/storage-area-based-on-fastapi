from typing import AsyncGenerator
from src.core.settings import database


async def get_db_session() -> AsyncGenerator:
    async with database.session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
