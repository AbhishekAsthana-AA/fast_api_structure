from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import BaseModel, ValidationError
from functools import lru_cache
import os
from pathlib import Path
env_path =  '.env'

load_dotenv(dotenv_path=env_path)



DATABASE_URL = os.getenv('DATABASE_URL')


class Settings():
    database_url = DATABASE_URL

@lru_cache
def get_setting():
    return Settings()
