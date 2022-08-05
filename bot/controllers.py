from bot.models import TelegramUser, Product
from telebot import types, TeleBot

from bot.tasks import parse_product
from db_redis import redis, scheduler
from logger import bot_logger, queue_logger
from rq import Queue


def get_all_products(user_id: int) -> str:
    products_names = [
        product.name for product in Product.get_all_products_by_user_id(user_id)
    ]

    bot_logger.info(
        f"Telegram User {TelegramUser.get_by_id(user_id).username} "
        f"get all products ({Product.count_user_products(user_id)})"
    )

    return ", ".join(products_names) or "Ничего не найдено"


def initialize_user(message: types.Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    if TelegramUser.get_by_id(user_id) is None:
        TelegramUser.create(
            user_id=user_id,
            username=username
        )

        bot_logger.info(
            f"Telegram User {message.from_user.username} has been registered."
        )

    TelegramUser.close_session()


def remove_product(message: types.Message, bot: TeleBot) -> None:
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

        bot_logger.info(
            f"Telegram User {message.from_user.username} "
            f"has deleted a product {message.text} "
            f"with id = {product.id}"
        )


def add_product(message: types.Message, bot: TeleBot) -> None:
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
        bot_logger.info(
            f"Telegram User {message.from_user.username} "
            f"have added a product {message.text} "
            f"with id = {product.id}"
        )

        queue = Queue("default", connection=redis)
        queue.enqueue(parse_product, product.name)

        queue_logger.info(
            f"A product {product.name} has been added to the queue."
        )

    else:
        bot.send_message(
            message.chat.id,
            "Вы не можете."
        )
