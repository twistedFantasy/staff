from celery import current_app


class register:
    """ Decorator for class tasks to name and register them. """

    def __call__(self, cls):
        cls.name = '%s.%s' % (cls.__module__, cls.__name__)
        try:
            current_app.tasks.register(cls())
        except Exception as e:
            print(e)  # FIXME: logger
        return cls
