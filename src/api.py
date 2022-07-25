from selenium import webdriver

from src.settings import DRIVER_EXECUTABLE_PATH


class API:
    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            executable_path=DRIVER_EXECUTABLE_PATH,
            options=options
        )

    def get(self):
        self.driver.get("https://www.avito.ru/krasnodar?q=freestyle+libre")
        return self.driver

    def __del__(self):
        self.driver.close()


