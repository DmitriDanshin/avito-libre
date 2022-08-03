from argparser import ArgParser
from datetime import datetime
from bot.base import bot
from app import App


def init_bot():
    print(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S\t|"),
        "Bot launched successfully"
    )
    bot.polling()


if __name__ == '__main__':
    app = App()
    arguments_parser = ArgParser()
    # app.run(arguments_parser.formats_to_save)
    init_bot()
