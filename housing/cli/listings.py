import json
from enum import Enum

import typer
from rich import print as rich_print

from housing.client import ListingsClient
from housing.config import settings

CSV_FILEPATH = settings.HOMEGATE_CSV_FILEPATH

listings = typer.Typer(no_args_is_help=True)


class Format(str, Enum):
    RICH = "rich"
    JSON = "json"


@listings.command(no_args_is_help=True)
def get(
    id: int = typer.Option(
        ...,
        "--id",
    ),
    format: Format = typer.Option(
        Format.RICH,
        "-f",
        "--format",
    ),
) -> None:
    listing = ListingsClient().get(id=id)
    if format == Format.RICH:
        rich_print(listing)
    elif format == Format.JSON:
        print(listing.json())


@listings.command()
def list(
    format: Format = typer.Option(
        Format.RICH,
        "-f",
        "--format",
    ),
) -> None:
    listings = ListingsClient().list()
    if format == Format.RICH:
        rich_print(listings)
    elif format == Format.JSON:
        print(json.dumps([l.dict() for l in listings]))
