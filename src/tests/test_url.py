from unittest import TestCase

from src.utils.url import URL


# todo объединить у себя две ветки на master
# todo создать новую ветку с название tests_url
# asserEqual
# asserNotEqual
# https://pythonworld.ru/moduli/modul-unittest.html
# todo удалить все комментарии после завершения

class TestURL(TestCase):
    # todo создать класс url
    # проверить несколько случаев
    # передать другой тип данных
    # передать url на русском языке
    # передать url без протокола
    # передать числа
    # передать другой протокол

    # Проверит на отсутствие протокола и сделать его не содержит domain
    # "httpm://yandex.ru"
    # todo создать множество web protocols(in settings)
    def test_url_prefix(self):
        pass

    def test_url(self):
        url = URL(
            domain="httpm://yandex.ru",
            path="Moscow",
            query={
                "q": "Hello world"
            }
        )
        self.assertEqual(str(url), "https://yandex.ru/moscow?q=hello+world")
        url = URL(
            domain="https://гугл.com",
            path="переводчик",
            query={
                "q": "Привет"
            }
        )
        url.domain = 'https://yandex.ru'
        self.assertEqual(str(url), "https://yandex.ru/moscow?q=hello+world")
        url2 = URL(
            domain="google.com",
            path="map",
            query={
                "q": "Krasnodar"
            }
        )
        url3 = URL(
            domain="https://'google'.com",
            path="'map'",
            query={
                "q": "'Moscow'"
            }
        )
        url4 = URL(
            domain="FTP://google.com",
            path="map",
            query={
                "q": "Moscow"
            }
        )

    def test_type_checking(self):
        url5 = URL(
            domain="[https://yandex.ru]",
            path="{fifa}",
            query={
                "q": '12312'
            }
        )
