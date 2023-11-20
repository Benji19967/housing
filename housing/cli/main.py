from enum import Enum

import pendulum
import typer

from housing.common import Row, get_new_listings, read_rows, write_row
from housing.config import settings
from housing.homegate import fetch_listings as homegate_fetch_listings

CSV_FILEPATH = settings.HOMEGATE_CSV_FILEPATH

housing = typer.Typer()


class Source(Enum):
    HOMEGATE = "homegate"
    FLATFOX = "flatfox"

    def __str__(self) -> str:
        return str(self.value)


@housing.command()
def main(
    source: Source = typer.Option(
        ...,
        "-s",
        "--source",
    ),
) -> None:
    print(f"{pendulum.now()}: checking for new listings on {source}.")

    current_rows = read_rows(CSV_FILEPATH)

    if source == Source.HOMEGATE:
        listings = homegate_fetch_listings()
    else:
        raise ValueError(f"Source {source} not supported yet.")

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
