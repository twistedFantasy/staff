import datetime


def cleanup(value):
    return value.lower().strip()


def format(value):
    return f'{value:%Y-%m-%d}'


def today():
    return datetime.datetime.now()


def true(value):
    return value in ['true', 'True', '1', True]
