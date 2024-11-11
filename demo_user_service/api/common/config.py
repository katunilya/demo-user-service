from pydantic import SecretStr
from pydantic_settings import BaseSettings


class APIConfig(BaseSettings):
    DEBUG: bool = True
    TITLE: str = "Demo User Service API"
    DESCRIPTION: str = "API for demonstrating work with DB"
    VERSION: str = "0.0.1"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: SecretStr = "admin"

    model_config = {
        "env_prefix": "API_",
    }
