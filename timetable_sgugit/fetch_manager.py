from threading import Thread
from time import sleep

from loguru import logger

from .controllers import DataFetcher


class FetchManager(Thread):

    def __init__(self, data_fetcher: DataFetcher) -> None:
        super().__init__(daemon=True)
        self.data_fetcher = data_fetcher
        self.name = 'FetchManager'


    def run(self):
        while True:
            logger.info('awake FetchManager')
            with logger.catch(Exception, message='Ошибка при получении списка занятий', level='ERROR', reraise=False):
                self.data_fetcher.fetch_lessons()

            logger.info('FetchManager gonna sleep for 3 days. zzzz...')
            sleep(3 * 24 * 60 * 60)


    def join(self, timeout = None) -> None:
        if hasattr(self, 'loop'):
            self.loop.stop()

        return super().join(timeout)
