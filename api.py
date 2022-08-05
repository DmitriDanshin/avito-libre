from selenium.webdriver import FirefoxProfile, Firefox
from webdriver_manager.firefox import GeckoDriverManager
import settings
import os
from utils.url import URL


class API:
    def __init__(self):
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference("browser.display.use_document_fonts", 0)

        os.environ['MOZ_HEADLESS'] = '1'

        self.driver = Firefox(
            executable_path=self.__install_firefox_driver(),
            firefox_profile=firefox_profile
        )

    @staticmethod
    def __install_firefox_driver():
        return GeckoDriverManager().install()

    def get(self, url: URL):
        self.driver.get(str(url))
        return self.driver

    def __del__(self):
        if not settings.DEBUG:
            self.driver.close()
