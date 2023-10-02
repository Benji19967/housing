import time
from typing import List

import cloudscraper
import pendulum
import requests
import typer
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from housing.common import Listing, Row, get_new_listings, read_rows, write_row
from housing.config import settings

RADIUS_METERS = 2000
LOCATION = "city-zug"
LISTINGS_URL = f"https://www.homegate.ch/rent/real-estate/{LOCATION}/matching-list?ep={{page_number}}&be={RADIUS_METERS}"

CSV_FILEPATH = settings.HOMEGATE_CSV_FILEPATH

housing = typer.Typer()

import undetected_chromedriver as uc


def fetch_listings() -> List[Listing]:
    """
    Fetch listings from HTML page.

    The "TOP" listings are stored differently than
    regular listings.

    Each page contains at most 20 listings, hence we
    fetch multiple pages until we get to a page with no listings.
    """
    listings: List[Listing] = []
    """ driver = webdriver.Chrome() """
    driver = uc.Chrome(headless=True,use_subprocess=False)
    url = "https://www.homegate.ch/rent"

    for page_number in range(1, 10):
        driver.execute_script(f"window.open('https://www.homegate.ch/rent','_blank');") # open page in new tab
        time.sleep(20) # wait until page has loaded
        driver.switch_to.window(window_name=driver.window_handles[0])   # switch to first tab
        driver.close() # close first tab
        driver.switch_to.window(window_name=driver.window_handles[0] )  # switch back to new tab
        time.sleep(2)
        driver.get("https://google.com")
        time.sleep(2)
        driver.get(url) # this should pass cloudflare captchas now
        html_text = driver.get("https://www.homegate.ch/rent/real-estate/matching-list")
        """ time.sleep(20) """
        """ print("Done sleep") """
        """ WebDriverWait(driver, 20).until( """
        """     EC.frame_to_be_available_and_switch_to_it( """
        """         ( """
        """             By.CSS_SELECTOR, """
        """             "iframe[title='Widget containing a Cloudflare security challenge']", """
        """         ) """
        """     ) """
        """ ) """
        """ print("Done wait 1") """
        """ WebDriverWait(driver, 20).until( """
        """     EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label")) """
        """ ).click() """
        """ print("Done wait 2") """

        """ soup = BeautifulSoup(html_text, "html.parser") """
        soup0 = BeautifulSoup(driver.page_source, "lxml")
        soup1 = BeautifulSoup(driver.name, "lxml")
        soup2 = BeautifulSoup(driver.title, "lxml")

        count_for_page = 0

        """ if not soup.body: """
        """     raise ValueError("Could not find body") """
        print(soup0.body)
        print(soup1.body)
        print(soup2.body)

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


@housing.command()
def main(
    website: str = typer.Option(
        ...,
        "--website",
    )
) -> None:
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
    housing()
