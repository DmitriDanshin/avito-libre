from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bot.models import (
    Base, TelegramUser,
    SessionCore, Product
)


class TestModels(TestCase):

    def setUp(self) -> None:
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(bind=self.engine)
        Base.metadata.create_all(self.engine)
        SessionCore.change_session(self.session)

    def test_create_telegram_user(self):
        first = TelegramUser(id=1, username="Adolf")
        second = TelegramUser.create(user_id=1, username="Adolf")
        self.assertEqual(first, second)
        self.assertIsNot(first, second)

    def test_integrity_telegram_user(self):
        with self.assertRaises(IntegrityError):
            TelegramUser.create(user_id=1, username="Adolf")
            TelegramUser.create(user_id=1, username="Adolf")

    def test_get_by_id_telegram_user(self):
        first = TelegramUser.create(user_id=1, username="Adolf")
        second = TelegramUser.create(user_id=2, username="Ivan")
        self.assertEqual(first, TelegramUser.get_by_id(1))
        self.assertNotEqual(second, TelegramUser.get_by_id(1))

    def test_get_all_telegram_user(self):
        first = TelegramUser.create(user_id=1, username="Adolf")
        second = TelegramUser.create(user_id=2, username="Vladimir")
        self.assertEqual(TelegramUser.all(), [first, second])

    def test_create_product(self):
        product1 = Product(id=1, name='Ivan', city='Moscow')
        product2 = Product.create(user_id=1, name='Ivan', city='Moscow')
        self.assertNotEqual(product1, product2)

    def test_delete_product(self):
        product1 = Product.create(user_id=1, name='Ivan')
        self.assertEqual(Product.delete(product1), None)

    def test_count_product(self):
        for user_id in range(10):
            Product.create(user_id=user_id, name='Ivan')
        self.assertEqual(Product.count(), 10)

    def test_get_by_name_product(self):
        product1 = Product.create(user_id=1, name='Libre')
        product2 = Product.create(user_id=2, name='matiz')
        self.assertEqual(Product.get_by_name('libre'), product1)
        self.assertEqual(Product.get_by_name('Matiz'), product2)

    def test_get_all_by_user_id_product(self):
        TelegramUser.create(user_id=1, username='Максимка')
        first = Product.create(user_id=1, name='Libre')
        second = Product.create(user_id=1, name='Matiz')

        self.assertEqual(
            [first, second],
            list(Product.get_all_products_by_user_id(user_id=1))
        )

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
