import csv
import datetime
import pathlib
from typing import Any, Iterable, List

import pendulum
import requests
from bs4 import BeautifulSoup
from pendulum import parse as pendulum_parse  # type: ignore
from pendulum.datetime import DateTime
from pydantic import BaseModel

from housing.config import settings

RADIUS_METERS = 2000
LOCATION = "city-zug"
LISTINGS_URL = f"https://www.homegate.ch/rent/real-estate/{LOCATION}/matching-list?ep={{page_number}}&be={RADIUS_METERS}"

CSV_FILEPATH = settings.HOMEGATE_CSV_FILEPATH


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


def fetch_listings() -> List[Listing]:
    """
    Fetch listings from HTML page.

    The "TOP" listings are stored differently than
    regular listings.

    Each page contains at most 20 listings, hence we 
    fetch multiple pages until we get to a page with no listings.
    """
    listings: List[Listing] = []

    for page_number in range(1, 10):
        html_text = requests.get(LISTINGS_URL.format(page_number=page_number)).text
        soup = BeautifulSoup(html_text, "html.parser")

        count_for_page = 0

        if not soup.body:
            raise ValueError("Could not find body")

        a_top = soup.body.find_all("a", {"data-test": "result-list-item"}, href=True)
        result_list_items_regular = soup.body.find_all(
            "div", {"data-test": "result-list-item"}
        )
        a_regular = [item.find("a", href=True) for item in result_list_items_regular]

        for a in a_top + a_regular:
            listing_id = a["href"].replace("/rent/", "")
            listings.append(Listing(id=listing_id))
            count_for_page += 1
        if count_for_page == 0:
            break

    return listings


def get_new_listings(new_row: Row, previous_row: Row) -> List[Listing]:
    """
    Check if the listings we fetched contains new listings
    compared to the listings we fetched in the last run.
    """
    new_listings = set(new_row.listings) - set(previous_row.listings)
    return list(new_listings)


def main() -> None:
    print(f"{pendulum.now()}: checking for new listings on homegate.")

    current_rows = read_rows(CSV_FILEPATH)

    listings = fetch_listings()

    new_row = Row(
        timestamp=pendulum.now(),
        num_listings=len(listings),
        listings=listings,
    )

    if not current_rows:
        write_row(filename=CSV_FILEPATH, row=new_row)
        return

    new_listings = get_new_listings(new_row=new_row, previous_row=current_rows[-1])
    if new_listings:
        print(f"Found new listings: {new_listings}")
        write_row(filename=CSV_FILEPATH, row=new_row)


if __name__ == "__main__":
    main()
