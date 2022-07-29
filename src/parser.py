from typing import Iterator

from selenium.webdriver.remote.webelement import WebElement
from selenium.common import JavascriptException

from src import settings
from src.utils.date_handler import DateHandler
from selenium.webdriver.common.by import By

from src.utils.script_handler import ScriptHandler
from src.utils.url import URL
from api import API

from src.settings import (
    DOMAIN, CITY, SEARCH,
    CARD_CLASS_NAME, MAIN_CONTAINER_CLASS,
    CARD_TITLE_CLASS_NAME, CARD_PRICE_CLASS_NAME,
    CARD_LOCATION_CLASS_NAME, CARD_DESCRIPTION_CLASS_NAME,
    CARD_DATE_CLASS_NAME, CARD_DATE_POPUP_CLASS_NAME,
    PAGINATOR_CLASS_NAME, PAGINATOR_ITEM_CLASS_NAME,
    PAGINATOR_FIRST_ITEM_INDEX, PAGINATOR_LAST_ITEM_INDEX
)


class Parser:
    def __init__(self):
        self.__url = URL(
            domain=DOMAIN,
            path=CITY,
            query={
                "q": SEARCH,
            }
        )
        self.__api = API()
        self.__handled_data = self.__handle_data()

    @property
    def data(self):
        return self.__handled_data

    def __click_to_all_card_dates(self, class_date_name, elements):
        # "scripts/simulation_mouse_click.js"
        scripts = ScriptHandler.read()
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
                "return arguments[0]"
                ".getElementsByClassName('arguments[1]')[0]"
                ".textContent;", element, class_name
            )
        except JavascriptException:
            return ""

    def __get_element_inner_html(self, element: WebElement):
        return self.__webdriver.execute_script(
            "return arguments[0].innerHTML;",
            element
        )

    def __make_cards_data(self, elements: list[WebElement]) -> Iterator[dict[str, str]]:
        return {
            (card_data := self.__make_card_data(card_element))['url']: card_data
            for card_element in elements
        }

    def __get_pagination_range(self) -> range:
        self.__webdriver = self.__api.get(self.__url)
        paginator_element = self.__webdriver.find_element(
            By.CLASS_NAME,
            PAGINATOR_CLASS_NAME
        )
        paginator_items = paginator_element.find_elements(
            By.CLASS_NAME,
            PAGINATOR_ITEM_CLASS_NAME
        )
        first_page = int(
            paginator_items[PAGINATOR_FIRST_ITEM_INDEX].text
        ) if not settings.DEBUG else 1
        last_page = int(
            paginator_items[PAGINATOR_LAST_ITEM_INDEX].text
        ) if not settings.DEBUG else 1

        return range(first_page, last_page + 1)

    def __handle_data(self):
        data = {}
        for i in self.__get_pagination_range():
            data |= self.__handle_page_data(i)
        return data

    def __handle_page_data(self, page: int) -> Iterator[dict[str, str]]:
        self.__url.query['p'] = str(page)
        self.__webdriver = self.__api.get(self.__url)

        elements = (
            self.__webdriver
            .find_element(By.CLASS_NAME, MAIN_CONTAINER_CLASS)
            .find_elements(
                By.CLASS_NAME, CARD_CLASS_NAME
            )
        )

        self.__click_to_all_card_dates(
            CARD_DATE_CLASS_NAME,
            elements
        )

        return self.__make_cards_data(elements)
