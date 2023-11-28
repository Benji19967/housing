import typer

from housing.cli import listings, scrape
from housing.config import settings

CSV_FILEPATH = settings.HOMEGATE_CSV_FILEPATH

housing = typer.Typer(no_args_is_help=True)

housing.add_typer(listings.listings, name="listings")
housing.add_typer(scrape.scrape, name="scrape")


if __name__ == "__main__":
    housing()
