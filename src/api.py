from utils.driver import get_driver_path
from selenium import webdriver


class API:
    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        print(get_driver_path())
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            executable_path=get_driver_path(),
            options=options
        )

    def get(self):
        self.driver.get("https://www.avito.ru/krasnodar?q=freestyle+libre")
        return self.driver

    def __del__(self):
        self.driver.close()
