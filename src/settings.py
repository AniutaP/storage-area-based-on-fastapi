from src.configs import setup_configs
from src.database.database import setup_database


configs = setup_configs()

database = setup_database(
    url=configs.db_configs.url.unicode_string(), echo=configs.db_configs.echo
)
