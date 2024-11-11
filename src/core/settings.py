from src.core.configs import setup_configs
from src.database.database import setup_database
from hawkcatcher import Hawk
import os
from dotenv import load_dotenv


load_dotenv()

hawk = Hawk(os.getenv('HAWK'))

configs = setup_configs()

database = setup_database(url=configs.db_configs.url)
