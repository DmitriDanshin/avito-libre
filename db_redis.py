from redis import Redis, AuthenticationError, ConnectionPool
from rq_scheduler import Scheduler

from logger import queue_logger

try:
    pool = ConnectionPool(host='localhost', port=6379, db=0)
    redis = Redis(connection_pool=pool)
    queue_logger.info(
        f"Redis client initialized successfully. "
        f"Redis version == {redis.info()['redis_version']}"
    )
    scheduler = Scheduler(connection=redis)
except AuthenticationError:
    queue_logger.critical(
        f"Redis cannot connect to the server. Authentication required."
    )
