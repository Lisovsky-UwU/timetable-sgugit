import sys
from loguru import logger


def init_logger():
    logger.remove()

    log_config = {
        'format': '{time:HH:mm:ss.SSS} | <lvl>[{level}]</lvl> | <{thread.name}>::{file}({line}) | <lvl>{message}</lvl>'
    }

    logger.add('log\\{time:YYYY-MM-DD}.log', retention="10 days", **log_config)
    logger.add(sys.stdout, **log_config)
