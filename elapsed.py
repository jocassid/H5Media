
from datetime import datetime, timedelta
from logging import DEBUG, Logger, basicConfig, getLogger
from time import sleep


class Elapsed:
    def __init__(
            self,
            description: str,
            logger: Logger,
            time_in_log_message: bool = False,
            also_print: bool = False,
    ):
        self.start_time = None
        self.timedelta = None
        self.description = description
        self.logger = logger
        self.time_in_log_message = time_in_log_message
        self.also_print = also_print

    def __enter__(self):
        self.start_time = datetime.now()
        message = f"{self.description} started"
        self.logger.info(message)


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.timedelta = datetime.now() - self.start_time


def main():
    basicConfig(
        filename="app.log",
        level=DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logger = getLogger(__name__)


    with Elapsed(logger) as elapsed:
        sleep(3)


if __name__ == '__main__':
    main()
