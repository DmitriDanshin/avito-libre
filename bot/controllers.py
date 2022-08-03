from bot.models import TelegramUser, Product
from telebot import types, TeleBot


def get_all_products(user_id: int) -> str:
    products_names = [
        product.name for product in Product.get_all_products_by_user_id(user_id)
    ]
    return ", ".join(products_names) or "Ничего не найдено"


def initialize_user(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    if TelegramUser.get_by_id(user_id) is None:
        TelegramUser.create(
            user_id=user_id,
            username=username
        )

    TelegramUser.close_session()


def remove_product(message: types.Message, bot: TeleBot):
    product = Product.get_by_name(message.text)
    if product is None:
        bot.send_message(message.chat.id, "Объявление не найдено")
    else:
        Product.delete(product)
        bot.send_message(
            message.chat.id,
            f"Объявление с текстом *{message.text}* "
            f"успешно удалено\. "
            f"Теперь Вы отслеживаете "
            f"{get_all_products(user_id=message.from_user.id)}",
            parse_mode='MarkdownV2'
        )


def add_product(message: types.Message, bot: TeleBot):
    product = Product.create(
        user_id=message.from_user.id,
        name=message.text,
        city="Krasnodar"
    )
    if product:
        bot.send_message(
            message.chat.id,
            f"Объявление с текстом *{product.name}* "
            f"успешно добавлено\. "
            f"Теперь Вы отслеживаете: "
            f"*{get_all_products(user_id=message.from_user.id)}*",
            parse_mode='MarkdownV2'
        )
