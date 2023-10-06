"""Settings to configure the inference app."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to get access to e.g. environment variables in an elegant way,
    which can be accessed globally across the app.
    """

    class Config:
        env_file = ".env"
        case_sensitive = False

    DATA_LOCATION: str = "/project/data"
