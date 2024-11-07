from src.repositories.login import LoginRepository
from src.services.login import LoginService


login_repository = LoginRepository()
login_service = LoginService(login_repository)


def get_auth_service() -> LoginService:
    return login_service