from src.domains.users.dto.users import AdminDTO
from src.security.hasher.hasher import Hasher
from src.configs.settings import configs


admin = AdminDTO(
    email=configs.ADMIN_EMAIL,
    password=Hasher.get_password_hash(configs.ADMIN_PASSWORD)
)
