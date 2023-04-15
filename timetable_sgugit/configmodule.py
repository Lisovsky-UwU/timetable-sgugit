import os.path
import configparser
from pydantic import BaseModel


class Bot(BaseModel):

    token            : str
    feedback_send_to : str


class Parser(BaseModel):

    groups_url    : str
    audiences_url : str
    teachers_url  : str
    lessons_url   : str
    manager       : bool = True


class Log(BaseModel):

    level: str = 'INFO'
    retention: int = 7


class Config(BaseModel):

    bot    : Bot
    parser : Parser
    log    : Log


if not os.path.exists('config.ini'):
    print('Отсутствует конфигурационный файл "config.ini"')
    exit(0)

try:
    config_pars = configparser.ConfigParser()
    config_pars.read('config.ini')

    config = Config(
        bot    = Bot(**config_pars['BOT']),
        parser = Parser(**config_pars['PARSER']),
        log    = Log(**config_pars['LOG']) if 'LOG' in config_pars else Log()
    )

except KeyError as e:
    print(f'Ошибка чтения значения из конфига: {e}')
    exit(0)
