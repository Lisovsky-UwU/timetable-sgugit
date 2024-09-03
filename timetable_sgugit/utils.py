from datetime import date

from loguru import logger

from .exceptions import DataBaseException
from .orm import engine, Base


def create_db():
    try:
        logger.info('Создание таблиц в БД...')
        Base.metadata.create_all(engine)
        logger.success('Таблицы созданы.')
    except Exception as e:
        raise DataBaseException(f'Ошибка создания таблиц: {e}')


def format_audience_str(audience: str) -> str:
    if audience is None or audience == '':
        return 'Без аудитории'
    if audience.isdigit():
        return f'{audience} аудитория'
    else:
        return audience


def get_next_month(mont: int, year: int) -> str:
    result = date(year, mont, 1)
    try:
        result = result.replace(month=result.month + 1)
    except ValueError:
        result = result.replace(month=1, year=result.year + 1)

    return result.strftime('%m.%Y')


def get_prev_month(mont: int, year: int) -> str:
    result = date(year, mont, 1)
    try:
        result = result.replace(month=result.month - 1)
    except ValueError:
        result = result.replace(month=12, year=result.year - 1)

    return result.strftime('%m.%Y')


def get_week_number(_date: date) -> int:
    return (_date.isocalendar()[1] + 1) % 2 + 1
