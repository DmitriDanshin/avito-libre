from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bot.models import (
    Base, TelegramUser,
    SessionCore, ProductFile, Product
)


class TestModels(TestCase):

    # Model.get_by_id()
    # Model.create()
    # Model.all()
    # Model.update_by_id(model_id, {"field": new_value})
    # Model.delete(model_instance)
    # Model.count()
    # Model.create_many(<Iterable[Model]>)

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
        user1 = TelegramUser.create(user_id=1, username="Adolf")
        user2 = TelegramUser.create(user_id=2, username="Ivan")
        self.assertEqual(user1, TelegramUser.get_by_id(1))
        self.assertNotEqual(user2, TelegramUser.get_by_id(1))

    def test_get_all_telegram_user(self):
        user1 = TelegramUser.create(user_id=1, username="Adolf")
        user2 = TelegramUser.create(user_id=2, username="Vladimir")
        self.assertEqual(TelegramUser.all(), [user1, user2])

    def test_create_product(self):
        product1 = Product(id=1, name='Ivan', city='Moscow')
        product2 = Product.create(user_id=1, name='Ivan', city='Moscow')
        self.assertNotEqual(product1, product2)

    def test_delete_product(self):
        product1 = Product.create(user_id=1, name='Ivan')
        self.assertEqual(Product.delete(product1), None)

    def test_count_product(self):
        count = 0
        for user_id in range(10):
            Product.create(user_id=user_id, name='Ivan')
            count += 1
        self.assertEqual(Product.count(), count)

    def test_get_by_name_product(self):
        product1 = Product.create(user_id=1, name='Libre')
        product2 = Product.create(user_id=2, name='matiz')
        self.assertEqual(Product.get_by_name('libre'), product1)
        self.assertEqual(Product.get_by_name('Matiz'), product2)

    def test_get_all_by_user_id_product(self):
        Product.create(user_id=1, name='Libre')
        Product.create(user_id=1, name='Matiz')
        print(Product.get_all_products_by_user_id(user_id=1))

    def test_create_product_file(self):
        product_file1 = ProductFile(name='rtx', product_id=1)
        product_file2 = ProductFile.create(name='rtx', product_id=1)
        self.assertNotEqual(product_file1, product_file2)

    def test_update_product_file(self):
        product_file1 = ProductFile.create(name='rtx', product_id=2)
        self.assertEqual(ProductFile.update(product_id=2), product_file1)

    def test_create_or_update_product_file(self):
        product_file1 = ProductFile.create(name='rtx', product_id=2)
        print(ProductFile.create_or_update('rtx', 2))
        print(ProductFile.create_or_update('rtx', 2))

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
