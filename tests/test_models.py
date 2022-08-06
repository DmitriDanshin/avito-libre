from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bot.models import Base, TelegramUser, SessionCore


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

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

