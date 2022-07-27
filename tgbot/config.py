import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass(frozen=True)
class AdminCredentials:
    email: str
    password: str


@dataclass(frozen=True)
class I18N:
    domain: str
    locales_dir: Path


@dataclass(frozen=True)
class TgBot:
    token: str
    admins: list
    payment_token: str


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    db: DbConfig
    admin: AdminCredentials
    i18n: I18N


def load_config(path: str = None) -> Config:
    # load_dotenv(path)
    return Config(
        tg_bot=TgBot(
            token=os.getenv('BOT_TOKEN', '5135575762:AAEDgcUR-r4TYnC1IV-DAMt7L8hiZXdOjEY'),
            admins=[
                '353057906',
            ],
            payment_token=os.getenv('PAYMENT_TOKEN', '54321'),
        ),
        db=DbConfig(
            host=os.getenv('DB_HOST', 'localhost'),
            password=os.getenv('DB_PASSWORD', 'password'),
            user=os.getenv('DB_USER', 'user'),
            database=os.getenv('DB_NAME', 'database'),
        ),
        admin=AdminCredentials(
            password=os.getenv('PASSWORD', 'password'),
            email=os.getenv('EMAIL', 'email'),
        ),
        i18n=I18N(
            domain='tgbot',
            locales_dir=Path(__file__).parent / 'locales',
        ),
    )
