import pathlib
from functools import lru_cache
from pydantic import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / 'uploads'

class Settings(BaseSettings):
    debug: bool = False

    class Config:
        evv_file = ".env"


@lru_cache
def get_settings():
    return Settings()

DEBUG=get_settings().debug
