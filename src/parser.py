from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from api import API


class Parser:
    def __init__(self):
        self.__api = API()
        self.__webdriver_response: WebDriver = self.__api.get()
        self.__handled_data = self.__handle_data()

    @property
    def data(self):
        return self.__handled_data

    def __handle_data(self):
        return len(self.__webdriver_response.find_elements(By.CLASS_NAME, "iva-item-content-rejJg"))
