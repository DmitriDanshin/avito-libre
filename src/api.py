from src import settings
from src.settings import DOMAIN, CITY, SEARCH
from src.utils.driver import get_driver_path
from selenium import webdriver
from src.utils.url import URL


class API:
    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            executable_path=get_driver_path(),
            options=options
        )

    def get(self):
        url = URL(
            domain=DOMAIN,
            path=CITY,
            query={
                "q": SEARCH
            }
        )
        self.driver.get(str(url))
        return self.driver

    def __del__(self):
        if not settings.DEBUG:
            self.driver.close()
