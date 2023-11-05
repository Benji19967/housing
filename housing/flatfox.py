# from selenium.webdriver import Chrome
from bs4 import BeautifulSoup

# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
# chrome_options.add_argument("--headless=new")  # for Chrome >= 109
# chrome_options.add_argument("--headless")

import selenium_utils

if __name__ == "__main__":
    # driver = Chrome(options=chrome_options)
    driver = selenium_utils.driverInit()

    driver.get(
        "https://flatfox.ch/en/search/?east=8.680391&north=47.421354&query=Z%C3%BCrich&south=47.333591&west=8.392925"
    )

    soup = BeautifulSoup(driver.page_source, "lxml")
    for listing_id in soup.find_all("a", class_="listing-thumb-title"):
        print(listing_id)
