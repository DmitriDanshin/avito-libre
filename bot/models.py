from typing import Union, Iterable

from sqlalchemy import Column, Integer, String, ForeignKey
from db import get_session
from settings import (
    TELEGRAM_USERNAME_MAX_LENGTH,
    PRODUCT_CITY_MAX_LENGTH, PRODUCT_NAME_MAX_LENGTH,
    PRODUCT_FILE_NAME_MAX_LENGTH
)
from sqlalchemy.orm import declarative_base, relationship, Query

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
    def get_by_id(user_id: int) -> "TelegramUser":
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


class ProductFile(Base):
    __tablename__ = 'products_files'
    id = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name = Column(
        String(PRODUCT_FILE_NAME_MAX_LENGTH)
    )
    product_id = Column(
        Integer, ForeignKey("products.id")
    )

    @staticmethod
    def add_many(product_filenames: Iterable["ProductFile"]) -> None:
        session.add_all(product_filenames)
        session.commit()

    @staticmethod
    def get_all_files_by_product_id(product_id: id) -> Query:
        return (
            session
            .query(ProductFile)
            .filter_by(product_id=product_id)
        )


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

    files = relationship("ProductFile")

    @staticmethod
    def delete(product: "Product") -> None:
        session.delete(product)
        session.commit()

    @staticmethod
    def create(user_id: int, name: str, city: str = 'Krasnodar') -> Union["Product", None]:
        name = name.strip().lower()

        if name not in ExcludedProducts.as_set():
            product = Product(
                user_id=user_id,
                name=name,
                city=city
            )
            session.add(product)
            session.commit()
            return product

    @staticmethod
    def get_by_name(name: str) -> "Product":
        return (
            session
            .query(Product)
            .filter_by(name=name.strip().lower())
            .first()
        )

    @classmethod
    def get_all_products_by_user_id(cls, user_id: int) -> Query:
        return (
            session
            .query(Product)
            .filter_by(user_id=user_id)
        )

    @classmethod
    def count_user_products(cls, user_id: int) -> int:
        return cls.get_all_products_by_user_id(user_id).count()


class ExcludedProducts(Base):
    __tablename__ = 'excluded_products'
    id = Column(
        Integer, primary_key=True, autoincrement=True
    )
    name = Column(
        String(PRODUCT_NAME_MAX_LENGTH)
    )

    @staticmethod
    def as_set() -> set[str]:
        return {
            excluded_product.name for excluded_product
            in session.query(ExcludedProducts).all()
        }
