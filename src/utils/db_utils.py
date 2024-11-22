from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from functools import wraps


@dataclass
class IsolationLevels:

    rc: str = 'READ COMMITTED'
    rr: str = 'REPEATABLE READ'
    s: str = 'SERIALIZABLE'


def model_to_dict(model):
    return {col.name: getattr(model, col.name) for col in model.__table__.columns}


def set_isolation_level(isolation_level: str | None = None):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            db_session = [arg for arg in args if isinstance(arg, AsyncSession)][0]
            if isolation_level is not None:
                await db_session.execute(
                    text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
                )
            return await func(*args, **kwargs)
        return inner
    return wrapper
