from typing import Iterator

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common import JavascriptException
from selenium.webdriver.common.by import By

from src.utils.date_handler import DateHandler
from src.settings import (
    CARD_CLASS_NAME, MAIN_CITY_CLASS_NAME,
    CARD_TITLE_CLASS_NAME, CARD_PRICE_CLASS_NAME,
    CARD_LOCATION_CLASS_NAME, CARD_DESCRIPTION_CLASS_NAME,
    CARD_DATE_CLASS_NAME, CARD_DATE_POPUP_CLASS_NAME
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

    def __click_to_all_card_dates(self, class_date_name, elements):
        with open("scripts/simulation_mouse_click.js", "r") as scripts:
            scripts = scripts.read()
            for element in elements:
                self.__webdriver.execute_script(
                    scripts, element, class_date_name
                )

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
                .replace("\xa0", ' ')
            ),
            "location": self.__get_element_text_by_class_name(
                CARD_LOCATION_CLASS_NAME,
                card_element
            ),
            "url": self.__get_url_from_card_element(card_element),
            "date": self.__get_date(
                CARD_DATE_POPUP_CLASS_NAME,
                card_element
            )
        }

    @staticmethod
    def __handle_date(date: str):
        return DateHandler.reformat_date(date)

    def __get_date(self, class_name, card_element):
        date_element: WebElement = self.__webdriver.execute_script(
            "return arguments[0]"
            ".getElementsByClassName(arguments[1])[0];",
            card_element, class_name
        )
        if date_element is None:
            return date_element
        return self.__handle_date(date_element.text)

    def __get_url_from_card_element(self, card_element: WebElement):
        return self.__webdriver.execute_script(
            "return arguments[0]"
            ".querySelector('a')"
            ".href;", card_element
        )

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
        self.__click_to_all_card_dates(CARD_DATE_CLASS_NAME, elements)

        return self.__make_cards_data(elements)
