from sqlalchemy import Column, Integer, String, ForeignKey
from db import get_session
from settings import (
    TELEGRAM_USERNAME_MAX_LENGTH,
    PRODUCT_CITY_MAX_LENGTH,
    PRODUCT_NAME_MAX_LENGTH
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
session = get_session()


class TelegramUser(Base):
    __tablename__ = 'telegram_users'
    id = Column(Integer, primary_key=True)
    username = Column(
        String(TELEGRAM_USERNAME_MAX_LENGTH),
        nullable=False, unique=True
    )
    products = relationship("Product")

    @staticmethod
    def get_by_id(user_id: int):
        return (
            session.query(TelegramUser).get(user_id)
        )

    @staticmethod
    def create(user_id: int, username: str) -> None:
        user = TelegramUser(
            id=user_id, username=username
        )
        session.add(user)
        session.commit()

    @staticmethod
    def close_session():
        session.close()


class Product(Base):
    __tablename__ = 'products'
    id = Column(
        Integer, primary_key=True, autoincrement=True
    )
    city = Column(
        String(PRODUCT_CITY_MAX_LENGTH)
    )
    name = Column(
        String(PRODUCT_NAME_MAX_LENGTH)
    )
    user_id = Column(
        Integer, ForeignKey("telegram_users.id")
    )

    @staticmethod
    def delete(product: 'Product') -> None:
        session.delete(product)
        session.commit()

    @staticmethod
    def create(user_id: int, name: str, city: str = 'Krasnodar'):
        product = Product(
            user_id=user_id,
            name=name.strip().lower(),
            city=city
        )
        session.add(product)
        session.commit()

    @staticmethod
    def get_by_name(name: str):
        return (
            session.query(Product).filter_by(name=name.strip().lower()).first()
        )

    @staticmethod
    def get_all_products_by_user_id(user_id: int):
        return (
            session.query(Product).filter_by(user_id=user_id)
        )