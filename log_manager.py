import logging
import queue

from logging.handlers import (
    QueueHandler,
    QueueListener,
    RotatingFileHandler,
)



def create_logger(path: str, name: str):
    log_queue = queue.Queue(maxsize=10_000)

    file_handler = RotatingFileHandler(
        path,
        maxBytes=20 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    queue_handler = QueueHandler(log_queue)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(queue_handler)
    logger.propagate = False

    listener = QueueListener(
        log_queue,
        file_handler,
    )

    listener.start()

    return logger, listener
