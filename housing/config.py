from pydantic import BaseSettings


class Settings(BaseSettings):
    HOMEGATE_CSV_FILEPATH: str

    class Config:
        env_file = "housing/.env"


settings = Settings()
