import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from os import system, name
import undetected_chromedriver as uc
from typing import Dict, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from housing.common import Listing

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
URL = "https://www.homegate.ch/rent/real-estate/city-{location}/matching-list?ag={min_price}&ah={max_price}"


def fetch_listings() -> List[Listing]:
    """
    Fetch listings from HTML page.

    The "TOP" listings are stored differently than
    regular listings.

    Each page contains at most 20 listings, hence we
    fetch multiple pages until we get to a page with no listings.
    """
    return []


def scroll_down(driver):
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        time.sleep(2)


def driverInit():
    # setting options for undetected chrome driver
    option = uc.ChromeOptions()
    option.add_argument("--log-level=3")
    option.add_argument("--disable-infobars")

    # option.add_argument("--headless")
    option.add_argument("--disable-extensions")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    }
    option.add_experimental_option("prefs", prefs)

    option.add_argument(f"user-agent={USER_AGENT}")
    driverr = uc.Chrome(options=option)
    return driverr


if __name__ == "__main__":
    location = input("Please enter location filter: ")
    location = location.lower()
    min_price = input("Please enter min price filter: ")
    max_price = input("Please enter max price filter: ")

    driver = driverInit()
    driver.get(
        URL.format(
            location=location,
            min_price=min_price,
            max_price=max_price,
        )
    )
    time.sleep(6)

    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    scroll_down(driver)
    raw_urls = driver.find_elements(
        By.XPATH,
        "(//div[@class='HgCardElevated_cardElevated_wE2UB']//a)",
    )
    listing_urls = []
    for raw_url in raw_urls:
        listing_urls.append(raw_url.get_attribute("href"))
    print(listing_urls)

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
    print(rooms)

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
    """ print(details) """

    # Ensure all lists have the same length
    if len(listing_urls) == len(prices) == len(locations) == len(titles):
        # Combine the data into an output list
        output_list = []
        for i in range(len(listing_urls)):
            sublist = [listing_urls[i], prices[i], locations[i], titles[i]]
            output_list.append(sublist)
        print(output_list)

    driver.quit()
