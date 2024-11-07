from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenPayloadDTO:
    sub: str | None = None
    exp: datetime | None = None
