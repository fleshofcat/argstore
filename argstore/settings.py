from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    init_not_existed_db: bool = False

    class Config:
        env_file = ".env", "../.env"
