from bot.handlers import menu, start
from functools import partial
from telebot import TeleBot

from settings import BOT_TOKEN


bot = TeleBot(BOT_TOKEN)

bot.register_message_handler(
    partial(start, bot=bot),
    commands=['start']
)

bot.register_message_handler(
    partial(menu, bot=bot),
    content_types=['text']
)

