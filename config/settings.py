# config/settings.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    WHISPER_MODEL: str = "ct2-whisper-small-ko"
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"
    WHISPER_MODEL_DIR: str = "./models"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

