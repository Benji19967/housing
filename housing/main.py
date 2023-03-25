from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
import pendulum
from pydantic import BaseModel
import datetime
from typing import Any, Iterable, List

import pathlib

RADIUS_METERS = 2000
LOCATION = "city-zug"
LISTINGS_URL = f"https://www.homegate.ch/rent/real-estate/{LOCATION}/matching-list?ep={{page_number}}&be={RADIUS_METERS}"

CSV_FILENAME = "homegate.csv"


class Listing(BaseModel):
    id: int

    class Config:
        frozen = True


class Row(BaseModel):
    timestamp: datetime.datetime
    num_listings: int
    listings: List[Listing]

    def to_cvs(self) -> Iterable[Any]:
        yield str(self.timestamp)
        yield self.num_listings
        for listing in self.listings:
            yield listing.id

    @classmethod
    def from_cvs(cls, row: List[str]) -> "Row":
        timestamp = pendulum.parse(row[0])
        num_listings = int(row[1])
        listings = [Listing(id=int(listing_id)) for listing_id in row[2:]]
        return Row(
            timestamp=timestamp,
            num_listings=num_listings,
            listings=listings,
        )


def read_rows(filename: str) -> List[Row]:
    file = pathlib.Path(filename)
    if not file.exists():
        return []

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        return [Row.from_cvs(row=row) for row in reader]


def write_row(filename: str, row: Row) -> None:
    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(row.to_cvs())


def fetch_listings() -> List[Listing]:
    listings: List[Listing] = []

    for page_number in range(1, 10):
        html_text = requests.get(LISTINGS_URL.format(page_number=page_number)).text
        soup = BeautifulSoup(html_text, "html.parser")

        count = 0

        a_top = soup.body.find_all("a", {"data-test": "result-list-item"}, href=True)
        result_list_items_regular = soup.body.find_all(
            "div", {"data-test": "result-list-item"}
        )
        a_regular = [item.find("a", href=True) for item in result_list_items_regular]

        for a in a_top + a_regular:
            listing_id = a["href"].replace("/rent/", "")
            listings.append(Listing(id=listing_id))
            count += 1
        if count == 0:
            break

    return listings


def get_new_listings(new_row: Row, previous_row: Row) -> List[Listing]:
    new_listings = set(new_row.listings) - set(previous_row.listings)
    return list(new_listings)


def main():
    current_rows = read_rows(CSV_FILENAME)

    listings = fetch_listings()

    new_row = Row(
        timestamp=pendulum.now(), num_listings=len(listings), listings=listings
    )

    if not current_rows:
        write_row(filename=CSV_FILENAME, row=new_row)
        return

    new_listings = get_new_listings(new_row=new_row, previous_row=current_rows[-1])
    if new_listings:
        print(f"Found new listings: {new_listings}")
        write_row(filename=CSV_FILENAME, row=new_row)


if __name__ == "__main__":
    main()
