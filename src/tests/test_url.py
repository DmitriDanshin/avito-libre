from unittest import TestCase

from src.utils.url import URL


class TestURL(TestCase):
    def test_url_prefix(self):
        pass

    def test_url_empty(self):
        url = URL(
            domain="https://yandex.ru",
            path="Moscow",
            query={
                "q": "Hello world"
            }
        )

        self.assertEqual(str(url),
                         "https://yandex.ru/moscow?q=hello+world"
                         )
        url.domain = ''
        self.assertEqual(str(url),
                         "moscow?q=hello+world"
                         )
        url.path = ''
        self.assertEqual(str(url),
                         "?q=hello+world"
                         )
        url.query = {'q': ''}
        self.assertEqual(str(url),
                         "?q="
                         )

    def test_url_russian(self):
        url = URL(
            domain="https://гугл.com",
            path="переводчик",
            query={
                "q": "Привет"
            }
        )
        self.assertEqual(
            "https://гугл.com/переводчик?q=%d0%bf%d1%80%d0%b8%d0%b2%d0%b5%d1%82",
            str(url)
        )
        url.domain = 'https://озон.ру'
        self.assertEqual(
            "https://озон.ру/переводчик?q=%d0%bf%d1%80%d0%b8%d0%b2%d0%b5%d1%82",
            str(url)
        )
        url.path = "бытовая техника"
        self.assertEqual(
            "https://озон.ру/бытовая техника?q=%d0%bf%d1%80%d0%b8%d0%b2%d0%b5%d1%82",
            str(url)
        )
        url = URL(
            domain="https://гугл.com",
            path="переводчик"
        )
        url_lower = url
        url_upper = url

        url_lower.query = {"q": "телевизор"}
        url_upper.query = {"q": "Телевизор"}
        self.assertEqual(str(url_lower), str(url_upper))

    def test_url_data_type(self):
        url = URL(
            domain="https://google.com",
            path="map",
            query={
                "q": 'krasnodar'
            }
        )
        self.assertEqual(str(url),
                         "https://google.com/map?q=krasnodar"
                         )
        url.query = ''
        self.assertEqual(str(url),
                         "https://google.com/map"
                         )
        url.query = {1: 2}
        self.assertEqual(str(url),
                         "https://google.com/map?1=2"
                         )
        url.query = {1: [1, 2, 3]}
        self.assertEqual(str(url),
                         "https://google.com/map?1=%5b1%2c+2%2c+3%5d"
                         )
        url.query = {'q': (1, 2)}
        self.assertEqual(str(url),
                         "https://google.com/map?q=%281%2c+2%29"
                         )
