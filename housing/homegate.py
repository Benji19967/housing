import logging
import time
from typing import List

import selenium_utils
from selenium.webdriver.common.by import By

from housing.common import Listing

URL = "https://www.homegate.ch/rent/real-estate/city-{location}/matching-list?ag={min_price}&ah={max_price}"


logger = logging.getLogger(__name__)


class HomegateListing(Listing):
    price: str
    location: str
    title: str
    room: str | None = None
    space: str | None = None


def fetch_listings() -> List[Listing]:
    """
    Fetch listings from HTML page.
    """
    # location = input("Please enter location filter: ")
    # location = location.lower()
    # min_price = input("Please enter min price filter: ")
    # max_price = input("Please enter max price filter: ")
    location = "zurich"
    min_price = 100
    max_price = 10_000

    logger.info(f"Fetching listings for {__name__}")

    driver = selenium_utils.driverInit()
    driver.get(
        URL.format(
            location=location,
            min_price=min_price,
            max_price=max_price,
        )
    )
    time.sleep(6)

    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    selenium_utils.scroll_down(driver)

    raw_urls = driver.find_elements(
        By.XPATH,
        "(//div[@class='HgCardElevated_cardElevated_wE2UB']//a)",
    )
    listing_urls = []
    for raw_url in raw_urls:
        listing_urls.append(raw_url.get_attribute("href"))
    logger.info(listing_urls)
    # print(listing_urls)

    raw_prices = driver.find_elements(
        By.XPATH,
        "//span[@class='HgListingCard_price_sIIoV']",
    )
    prices = []
    for item in raw_prices:
        prices.append(item.text)
    print(prices)

    raw_rooms = driver.find_elements(
        By.XPATH,
        "//div[@class='HgListingRoomsLivingSpace_roomsLivingSpace_FiW9E']//span",
    )
    rooms = []
    for item in raw_rooms:
        rooms.append(item.text)
    print(rooms)

    raw_spaces = driver.find_elements(
        By.XPATH,
        "(//div[@class='HgListingRoomsLivingSpace_roomsLivingSpace_FiW9E']//span)[2]",
    )
    spaces = []
    for item in raw_spaces:
        spaces.append(item.text)
    print(spaces)

    raw_locations = driver.find_elements(
        By.XPATH,
        "//div[@class='HgListingCard_address_dbLZ8']//address",
    )
    locations = []
    for item in raw_locations:
        locations.append(item.text)
    print(locations)

    raw_titles = driver.find_elements(
        By.XPATH,
        "//p[@class='HgListingDescription_title_wfr04']",
    )
    titles = []
    for item in raw_titles:
        titles.append(item.text)
    print(titles)

    raw_details = driver.find_elements(
        By.XPATH,
        "//p[@class='HgListingDescription_large_Xytnw']",
    )
    details = []
    for item in raw_details:
        details.append(item.text)
    print(details)

    listings = []
    # Ensure all lists have the same length
    if len(listing_urls) == len(prices) == len(locations) == len(titles):
        # Combine the data into an output list
        output_list = []
        for i in range(len(listing_urls)):
            listing = HomegateListing(
                id=i,
                price=prices[i],
                location=locations[i],
                title=titles[i],
            )
            listings.append(listing)
            sublist = [listing_urls[i], prices[i], locations[i], titles[i]]
            output_list.append(sublist)
        print(output_list)

    driver.quit()
    return listings
