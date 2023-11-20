from sqlmodel import Session, SQLModel, create_engine

from housing import models  # needed to create the models in the DB
from housing.config import settings

# TODO: AsyncEngine
# https://github.com/testdrivenio/fastapi-sqlmodel-alembic/blob/main/project/app/db.py

engine = create_engine(settings.get_postgresql_url(), echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
