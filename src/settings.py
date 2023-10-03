"""Settings to configure the inference app."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = False

    DATA_LOCATION: str
    MODEL_NAME: str = "custom_model"
