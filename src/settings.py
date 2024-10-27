from src.configs import setup_configs
from src.database.database import setup_database


configs = setup_configs()

if configs.db_configs.dev_env == 'test':
    db_url = 'sqlite+aiosqlite:///test_db'
    database = setup_database(url=db_url)
else:
    database = setup_database(url=configs.db_configs.url)
