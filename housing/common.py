import csv
import datetime
import pathlib
from typing import Any, Iterable, List

from pendulum import parse as pendulum_parse  # type: ignore
from pendulum.datetime import DateTime
from pydantic import BaseModel


def parse_datetime(dt: str) -> DateTime:
    """
    Convert ISO string datetimes to pendulum DateTimes
    """
    timestamp = pendulum_parse(dt)
    assert isinstance(timestamp, DateTime)
    return timestamp


class Listing(BaseModel):
    """
    Each listing has a unique identifier number.

    The listings can be accessed via "homegate.ch/rent/<id>"
    """

    id: int

    class Config:
        frozen = True


class Row(BaseModel):
    """
    The results of a run get stored as a new row in a file
    if there are new listings.
    """

    timestamp: datetime.datetime
    num_listings: int
    listings: List[Listing]

    def to_csv(self) -> Iterable[Any]:
        yield str(self.timestamp)
        yield self.num_listings
        for listing in self.listings:
            yield listing.id

    @classmethod
    def from_csv(cls, row: List[str]) -> "Row":
        timestamp = parse_datetime(dt=row[0])
        num_listings = int(row[1])
        listings = [Listing(id=int(listing_id)) for listing_id in row[2:]]
        return Row(
            timestamp=timestamp,
            num_listings=num_listings,
            listings=listings,
        )


def read_rows(filename: str) -> List[Row]:
    """
    Read rows from log file.

    Log file is in CSV format.
    """
    file = pathlib.Path(filename)
    if not file.exists():
        return []

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        return [Row.from_csv(row=row) for row in reader]


def write_row(filename: str, row: Row) -> None:
    """
    Write rows to file in CSV format
    """
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(row.to_csv())


def get_new_listings(new_row: Row, previous_row: Row) -> List[Listing]:
    """
    Check if the listings we fetched contains new listings
    compared to the listings we fetched in the last run.
    """
    new_listings = set(new_row.listings) - set(previous_row.listings)
    return list(new_listings)
