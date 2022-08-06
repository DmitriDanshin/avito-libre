from datetime import datetime
from typing import Union, Iterable, Any

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, asc
from db import get_session
from settings import (
    TELEGRAM_USERNAME_MAX_LENGTH,
    PRODUCT_CITY_MAX_LENGTH, PRODUCT_NAME_MAX_LENGTH,
    PRODUCT_FILE_NAME_MAX_LENGTH
)
from sqlalchemy.orm import declarative_base, relationship, Query

Base = declarative_base()


class SessionCore:
    session = get_session()

    @classmethod
    def change_session(cls, new_session):
        cls.session = new_session

    @classmethod
    def close_session(cls):
        cls.session.close()


class TelegramUser(Base, SessionCore):
    __tablename__ = 'telegram_users'
    id = Column(Integer, primary_key=True)
    username = Column(
        String(TELEGRAM_USERNAME_MAX_LENGTH),
        nullable=False, unique=True
    )
    products = relationship("Product")

    @classmethod
    def get_by_id(cls, user_id: int) -> Union["TelegramUser", None]:
        return (
            cls.session.query(TelegramUser).get(user_id)
        )

    @classmethod
    def create(cls, user_id: int, username: str):
        user = TelegramUser(
            id=user_id, username=username
        )
        cls.session.add(user)
        cls.session.commit()
        return user

    @classmethod
    def all(cls) -> list["TelegramUser"]:
        return cls.session.query(TelegramUser).all()

    def __eq__(self, other: "TelegramUser"):
        return all(
            (self.username == other.username, self.id == other.id)
        )


class ProductFile(Base, SessionCore):
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

    updated_at = Column(
        DateTime, default=datetime.now
    )

    @classmethod
    def create_many(cls, product_filenames: Iterable["ProductFile"]) -> None:
        cls.session.add_all(product_filenames)
        cls.session.commit()

    @staticmethod
    def get_all_files_by_product_id(product_id: int) -> Query:
        return (
            session
            .query(ProductFile)
            .filter_by(product_id=product_id)
        )

    @staticmethod
    def create_or_update(name: str, product_id: int):
        product_file = session.query(ProductFile).filter_by(product_id=product_id).first()
        if product_file is None:
            product_file = ProductFile(
                name=name, product_id=product_id
            )
            session.add(product_file)
            session.commit()
            return product_file
        else:
            session.query(ProductFile).filter_by(product_id=product_id).update({
                "updated_at": datetime.now()
            })
            session.commit()
            return product_file


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
    def get_last_n(n: int = 5) -> list[Any]:
        return (
            session
            .query(Product)
            .join(ProductFile, Product.files)
            .order_by(asc(ProductFile.updated_at))
            .limit(n)
            .all()
        )

    @staticmethod
    def count():
        return (
            session
            .query(Product)
            .count()
        )

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
