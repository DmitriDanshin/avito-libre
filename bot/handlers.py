from bot.controllers import (
    add_product, remove_product,
    initialize_user, get_all_products
)
from functools import partial
from telebot import types
import telebot

from bot.models import Product


def start(message: types.Message, bot: telebot.TeleBot):
    initialize_user(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_product_button = types.KeyboardButton("Добавить объявление")
    delete_product_button = types.KeyboardButton("Удалить объявление")
    show_products_button = types.KeyboardButton("Посмотреть отслеживаемые объявления")
    markup.row(add_product_button, delete_product_button, )
    markup.row(show_products_button)
    bot.send_message(
        message.chat.id,
        text=f"Привет, {message.from_user.first_name}! "
             f"Здесь Вы можете добавить объявления за "
             f"которыми нужно следить.",
        reply_markup=markup
    )


def menu(message: types.Message, bot: telebot.TeleBot):
    match message.text:
        case "Добавить объявление":
            sent = bot.send_message(
                message.chat.id,
                text="Введите название объявления, "
                     "которое нужно добавить:",
            )
            bot.register_next_step_handler(
                sent, partial(add_product, bot=bot)
            )
        case "Удалить объявление":
            if not len(list(Product.get_all_products_by_user_id(message.from_user.id))):
                bot.send_message(message.chat.id, "Нечего удалять")
            else:
                sent = bot.send_message(
                    message.chat.id,
                    text="Введите название объявления, "
                         "которое нужно удалить:",
                )
                bot.register_next_step_handler(
                    sent, partial(remove_product, bot=bot)
                )
        case "Посмотреть отслеживаемые объявления":
            bot.send_message(
                message.chat.id,
                text=get_all_products(message.from_user.id)
            )
