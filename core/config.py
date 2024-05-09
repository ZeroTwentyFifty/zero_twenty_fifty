import os
from pathlib import Path

from dotenv import load_dotenv


"""
TODO: Replace all of this with https://docs.pydantic.dev/latest/concepts/pydantic_settings/
"""

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "ZeroTwentyFifty"
    PROJECT_VERSION: str = "0.0.1"

    POSTGRES_USER: str = os.getenv("PGUSER")
    POSTGRES_PASSWORD = os.getenv("PGPASSWORD")
    POSTGRES_SERVER: str = os.getenv("PGHOST")
    POSTGRES_PORT: str = os.getenv(
        "PGPORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("PGDATABASE")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 2  # in mins
    LOG_FILE: Path = Path(os.getenv("LOG_FILE", "logs.log"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")


settings = Settings()
