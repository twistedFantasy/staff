from celery import current_app

from ssm.core.helpers import get_logger


logger = get_logger(__name__)


class register:
    """ Decorator for class tasks to name and register them. """

    def __call__(self, cls):
        cls.name = f'{cls.__module__}.{cls.__name__}'
        try:
            current_app.tasks.register(cls())
        except Exception as e:
            logger.error(e, f'unable to register celery task {cls.name}')
        return cls
