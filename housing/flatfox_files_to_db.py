import json
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from housing import models  # needed to create the models in the DB
from housing.config import settings

engine = create_engine(settings.get_postgresql_url(), echo=True)

DIR_FILES = "flatfox_listings"
FILE_FORMAT = "flatfox_listings_100_{i}.json"
NUM_FILES = 260


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def transfer_listings():
    for file_idx in range(NUM_FILES):
        FILENAME = Path(DIR_FILES) / FILE_FORMAT.format(i=file_idx)

        with open(FILENAME) as f:
            data = json.loads(f.read())
            listings = data["results"]

            with Session(engine) as session:
                for listing in listings:
                    listing = models.Listing(**listing)
                    session.add(listing)
                session.commit()


if __name__ == "__main__":
    create_db_and_tables()
    transfer_listings()
