from functools import partial

from telebot import types

from bot.controllers import add_product, remove_product


def start(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_product_button = types.KeyboardButton("Добавить объявление")
    delete_product_button = types.KeyboardButton("Удалить объявление")
    markup.add(
        add_product_button,
        delete_product_button
    )
    bot.send_message(
        message.chat.id,
        text=f"Привет, {message.from_user.first_name}! "
             f"Здесь Вы можете добавить объявления за "
             f"которыми нужно следить.",
        reply_markup=markup
    )


def menu(message, bot):
    match message.text:
        case "Добавить объявление":
            sent = bot.send_message(
                message.chat.id,
                text="Введите название объявления, "
                     "которое нужно добавить:",
            )
            bot.register_next_step_handler(sent, partial(add_product, bot=bot))
        case "Удалить объявление":
            sent = bot.send_message(
                message.chat.id,
                text="Введите название объявления, "
                     "которое нужно удалить:",
            )
            bot.register_next_step_handler(sent, partial(remove_product, bot=bot))



