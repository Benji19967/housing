from enum import Enum

import pendulum
import typer

from housing.common import Listing, Row, get_new_listings, read_rows, write_row
from housing.config import settings
from housing.homegate import fetch_listings as homegate_fetch_listings

CSV_FILEPATH = settings.HOMEGATE_CSV_FILEPATH

housing = typer.Typer()


class Website(Enum):
    HOMEGATE = "homegate"
    FLATFOX = "flatfox"


@housing.command()
def main(
    website: Website = typer.Option(
        ...,
        "--website",
    )
) -> None:
    print(f"{pendulum.now()}: checking for new listings on {website}.")

    current_rows = read_rows(CSV_FILEPATH)

    if website == Website.HOMEGATE:
        listings = homegate_fetch_listings()
    else:
        raise ValueError(f"Website {website} not supported yet.")

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
    housing()
