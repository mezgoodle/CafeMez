from typing import List

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    admin_email: SecretStr
    admin_password: SecretStr
    token: SecretStr
    payment_token: SecretStr
    admins: List[str] = ["353057906"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
