from datetime import datetime

from rq_scheduler import Scheduler

from app import App
from bot.models import Product

from db_redis import redis
from logger import queue_logger
from rq import Queue


def parse_product(product_name: str):
    app = App()

    filenames = app.parse(
        {"csv": True},
        product_name
    )

    Product.update_filename(
        new_filename=filenames[0],
        product_name=product_name
    )

    queue_logger.info(
        f"Product with name {product_name} "
        f"successfully registered"
    )


def add_to_parse_queue():
    products = {
        product.name for product in Product.get_last_n(5)
    }

    queue = Queue("default", connection=redis)

    for product in products:
        queue.enqueue(parse_product, product)

    queue_logger.info(
        f"All products ({Product.count()}) "
        f"successfully added to queue"
    )


def streams_tasks(scheduler: Scheduler):
    scheduler.schedule(
        result_ttl=60,
        scheduled_time=datetime.utcnow(),
        func=add_to_parse_queue,
        interval=60
    )
