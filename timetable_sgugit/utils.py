from loguru import logger

from .exceptions import DataBaseException
from .orm import engine
from .orm import Base


def create_db():
    try:
        logger.info('Создание таблиц в БД...')
        Base.metadata.create_all(engine)
        logger.success('Таблицы созданы.')
    except Exception as e:
        raise DataBaseException(f'Ошибка создания таблиц: {e}')
