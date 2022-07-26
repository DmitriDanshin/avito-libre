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
    def test_url(self):
        url = URL(
            domain="https://yandex.ru",
            path="Moscow",
            query={
                "q": "Hello world"
            }
        )
        self.assertEqual(str(url), "https://yandex.ru/moscow?q=hello+world")

    def test_type_checking(self):
        pass
