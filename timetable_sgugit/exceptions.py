class TimetableSgugitException(Exception):
    '''Базовое исключение'''


class DataBaseException(TimetableSgugitException):
    '''Исключение при работе с БД'''
