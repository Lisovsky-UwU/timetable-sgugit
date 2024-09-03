import os
import sys

from loguru import logger


def init_logger(log_lvl: str = 'INFO', retention: int = 7, write_in_file: bool = True):
    logger.remove()

    log_config = {
        'format': '{time:HH:mm:ss.SSS} | <lvl>[{level}]</lvl> | <{thread.name}>::{file}({line}) | <lvl>{message}</lvl>',
        'level': log_lvl,
    }
    
    if write_in_file:
        logger.add(os.sep.join(['log', '{time:YYYY-MM-DD}.log']), retention=f'{retention} days', **log_config)
    
    logger.add(sys.stdout, **log_config)
