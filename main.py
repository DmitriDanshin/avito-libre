from argparser import ArgParser
from bot.base import bot
from app import App
from logger import bot_logger


def init_bot():
    bot_logger.info("Bot initialized successfully.")
    bot.polling()


if __name__ == '__main__':
    arguments_parser = ArgParser()
    init_bot()
