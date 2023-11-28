from pydantic import BaseSettings

POSTGRES_URL_FORMAT = "postgresql://{username}:{password}@{host}:{port}/{database_name}"


class Settings(BaseSettings):
    HOMEGATE_CSV_FILEPATH: str

    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE_NAME: str = "housing"
    POSTGRESQL_HOST: str = "localhost"
    POSTGRESQL_PORT: int = 5432

    def get_postgresql_url(self) -> str:
        """
        URL format: https://stackoverflow.com/questions/3582552/what-is-the-format-for-the-postgresql-connection-string-url
        """
        return POSTGRES_URL_FORMAT.format(
            username=self.POSTGRESQL_USERNAME,
            password=self.POSTGRESQL_PASSWORD,
            host=self.POSTGRESQL_HOST,
            port=self.POSTGRESQL_PORT,
            database_name=self.POSTGRESQL_DATABASE_NAME,
        )

    class Config:
        env_file = (".env", "housing/.env")


settings = Settings()
