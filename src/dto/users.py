from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int | None = None
    name: str | None = None
    email: str | None = None
    password: str | None = None
    is_superuser: bool | None = None
    is_active: bool | None = None


@dataclass
class AdminDTO(UserDTO):
    is_superuser: bool = True
