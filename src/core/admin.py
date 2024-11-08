from src.dto.users import AdminDTO
from src.core.security import Hasher
from src.core.settings import configs


admin = AdminDTO(
    email=configs.ADMIN_EMAIL,
    password=Hasher.get_password_hash(configs.ADMIN_PASSWORD)
)
