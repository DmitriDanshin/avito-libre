from telebot import types
import telebot

from bot.models import TelegramUser, Product, session

tracked = []


def get_all_products(user_id: int) -> str:
    products_names = [
        product.name for product in Product.get_all_products_by_user_id(user_id)
    ]
    return ", ".join(products_names) or "Ничего не найдено"


def initialize_user(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    if TelegramUser.get_by_id(user_id) is None:
        user = TelegramUser(
            id=user_id, username=username
        )

        session.add(user)
        session.commit()

    session.close()


def remove_product(message: types.Message, bot: telebot.TeleBot):
    product = Product.get_by_name(message.text)
    if product is None:
        bot.send_message(message.chat.id, "Объявление не найдено")
    else:
        session.delete(product)
        session.commit()
        bot.send_message(
            message.chat.id,
            f"Объявление с текстом {message.text} "
            f"успешно удалено. "
            f"Теперь Вы отслеживаете "
            f"{get_all_products(user_id=message.from_user.id)}"
        )


def add_product(message: types.Message, bot: telebot.TeleBot):
    product = Product(
        user_id=message.from_user.id,
        name=message.text.strip().lower(),
        city="Krasnodar"
    )

    session.add(product)
    session.commit()

    bot.send_message(
        message.chat.id,
        f"Объявление с текстом {message.text} "
        f"успешно добавлено. "
        f"Теперь Вы отслеживаете: "
        f"{get_all_products(user_id=message.from_user.id)}"
    )
