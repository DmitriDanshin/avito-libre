from webdriver_manager.chrome import ChromeDriverManager
import settings
from selenium import webdriver
from utils.url import URL


class API:
    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values": {
                "images": 2,
            },
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            self.__install_chrome_driver(),
            options=options
        )

    @staticmethod
    def __install_chrome_driver():
        return ChromeDriverManager().install()

    def get(self, url: URL):
        self.driver.get(str(url))
        return self.driver

    def __del__(self):
        if not settings.DEBUG:
            self.driver.close()
