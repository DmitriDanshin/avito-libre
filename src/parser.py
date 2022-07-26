from typing import Iterator

from selenium.common import JavascriptException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from src.settings import (
    CARD_CLASS_NAME, MAIN_CITY_CLASS_NAME,
    CARD_TITLE_CLASS_NAME, CARD_PRICE_CLASS_NAME,
    CARD_LOCATION_CLASS_NAME, CARD_DESCRIPTION_CLASS_NAME
)

from api import API


class Parser:
    def __init__(self):
        self.__api = API()
        self.__webdriver: WebDriver = self.__api.get()
        self.__handled_data = self.__handle_data()

    @property
    def data(self):
        return self.__handled_data

    def __make_card_data(self, card_element: WebElement) -> dict[str, str]:
        return {
            "title": self.__get_element_text_by_class_name(
                CARD_TITLE_CLASS_NAME,
                card_element
            ),
            "price": (
                self.__get_element_text_by_class_name(
                    CARD_PRICE_CLASS_NAME,
                    card_element
                )
                .replace("\xa0", '')
            ),
            "description": (
                self.__get_element_text_by_class_name(
                    CARD_DESCRIPTION_CLASS_NAME,
                    card_element
                )
                .replace("\n", ' ')
            ),
            "location": self.__get_element_text_by_class_name(
                CARD_LOCATION_CLASS_NAME,
                card_element
            ),
        }

    def __get_element_text_by_class_name(self, class_name: str, element: WebElement) -> str:
        try:
            return self.__webdriver.execute_script(
                f"return arguments[0]"
                f".getElementsByClassName('{class_name}')[0]"
                f".textContent;", element
            )
        except JavascriptException:
            return ""

    def __get_element_inner_html(self, element: WebElement):
        return self.__webdriver.execute_script(
            "return arguments[0].innerHTML;",
            element
        )

    def __make_cards_data(self, elements: list[WebElement]) -> Iterator[dict[str, str]]:
        return (
            self.__make_card_data(card_element) for card_element in elements
            if MAIN_CITY_CLASS_NAME in self.__get_element_inner_html(card_element)
        )

    def __handle_data(self) -> Iterator[dict[str, str]]:
        elements = (
            self.__webdriver
            .find_elements(
                By.CLASS_NAME, CARD_CLASS_NAME
            )
        )

        return self.__make_cards_data(elements)
