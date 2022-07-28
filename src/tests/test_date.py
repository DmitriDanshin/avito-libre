from datetime import datetime
from unittest import TestCase

from src.utils.date_handler import DateHandler


class TestDate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.months = DateHandler.months_locales

    def test_date_correct(self):
        for i, month in enumerate(self.months):
            self.assertEqual(
                datetime(2022, i + 1, 14, 16, 48),
                DateHandler.reformat_date(f'14 {month} 16:48')
            )

    def test_date_incorrect(self):
        with self.assertRaises(ValueError):
            DateHandler.reformat_date('2018 апрель 25 11:15')
            # todo вынести в отдельный assertRaises
            # DateHandler.reformat_date('14.11.2005 16:48')
            #
            # DateHandler.reformat_date('27 июль 11:15')
            # DateHandler.reformat_date('26.09.2001')
            # DateHandler.reformat_date('12 12')

        with self.assertRaises(ValueError):
            DateHandler.reformat_date('27 июля 25 11:15')

    def test_date_empty(self):
        with self.assertRaises(TypeError):
            DateHandler.reformat_date()
