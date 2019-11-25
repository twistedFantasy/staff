import logging
from datetime import date, datetime, timedelta


FORMAT = '%Y-%m-%d'


def cleanup(value: str) -> str:
    return value.lower().strip()


def format(value: date) -> str:
    return f'{value:{FORMAT}}'


def today() -> date:
    return datetime.now().date()


def true(value: str) -> bool:
    return value in ['true', 'True', '1', 'yes', 'on']


def to_list(s, sep=',', filter=(None, '', {}, [])) -> list:
    if s in filter:
        return []
    if isinstance(s, str):
        ls = [item.strip() for item in s.split(sep)]
    else:
        ls = list(s)
    return [item for item in ls if item not in filter]

def delimit(l, sep=',', filter=(None, '', {}, [])):
    items = [i for i in to_list(l, sep, filter)]
    return sep.join([str(x) for x in items])


def pluralize(count, singular, plural=None):
    if count == 1:
        return singular
    return plural or (singular + 's')


def get_logger(path):
    return logging.getLogger(path)


def workdays(start: date, end: date, excluded: tuple = (6, 7)):
    days = []
    while start <= end:
        if start.isoweekday() not in excluded:
            days.append(start)
        start += timedelta(days=1)
    return days


class Day:

    def __init__(self, ago: int = 0, format: str = FORMAT, obj: object = None):
        self.obj = self if obj is None else obj
        self.format = format
        self.ago = ago
        self.set(ago)

    def __str__(self):
        return self.obj.day

    def set(self, ago):
        ago = int(ago)
        if isinstance(getattr(self.obj, 'date', None), date):
            start = self.obj.date
        else:
            start = today()

        if ago >= 0:
            self.obj.date = start - timedelta(days=ago)
        else:
            self.obj.date = start + timedelta(days=ago)
        self.obj.day = self.obj.date.strftime(self.format)
