from .exceptions import DataBaseException
from .orm import engine
from .orm import Base


def create_db():
    try:
        print('Создание таблиц в БД...')
        Base.metadata.create_all(engine)
        print('Таблицы созданы.')
    except Exception as e:
        raise DataBaseException(f'Ошибка создания таблиц: {e}')
