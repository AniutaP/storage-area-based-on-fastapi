from src.repositories.users import UserRepository
from src.services.login import LoginService


user_repository = UserRepository()
login_service = LoginService(user_repository)


def get_auth_service() -> LoginService:
    return login_service
