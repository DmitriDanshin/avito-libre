from argparser import ArgParser
from bot.base import bot
from bot.tasks import streams_tasks
from db_redis import scheduler
from logger import bot_logger


def init_bot():
    bot_logger.info("Bot initialized successfully.")
    bot.polling()


if __name__ == '__main__':
    arguments_parser = ArgParser()

    for job in scheduler.get_jobs():
        job.delete()

    streams_tasks(scheduler)

    init_bot()
