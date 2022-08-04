import logging
import sys
from pathlib import Path
from settings import LOGGER_FORMAT


def setup_logger(name: str, log_file: Path, level=logging.DEBUG):
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(
        logging.Formatter(fmt=LOGGER_FORMAT)
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(
        logging.Formatter(fmt=LOGGER_FORMAT)
    )

    logger_setup = logging.getLogger(name)
    logger_setup.setLevel(level)
    logger_setup.addHandler(file_handler)
    logger_setup.addHandler(stream_handler)

    return logger_setup


app_logger = setup_logger('APP', Path('logs/app.log'))
bot_logger = setup_logger('BOT', Path('logs/bot.log'))
writer_logger = setup_logger('WRITER', Path('logs/writer.log'))
parser_logger = setup_logger('PARSER', Path('logs/parser.log'))
queue_logger = setup_logger('QUEUE', Path('logs/queue.log'))



