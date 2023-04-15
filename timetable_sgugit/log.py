import sys
from loguru import logger
from .configmodule import config


def init_logger():
    logger.remove()

    log_config = {
        'format': '{time:HH:mm:ss.SSS} | <lvl>[{level}]</lvl> | <{thread.name}>::{file}({line}) | <lvl>{message}</lvl>',
        'level': config.log.level,
    }

    logger.add('log\\{time:YYYY-MM-DD}.log', retention=f'{config.log.retention} days', **log_config)
    logger.add(sys.stdout, **log_config)
