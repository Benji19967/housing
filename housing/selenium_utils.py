import undetected_chromedriver as uc
import time

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"


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
