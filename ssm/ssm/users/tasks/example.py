from celery import Task

from ssm.core.manage import register


@register()
class Example(Task):
    abstract = False

    def run(self, *args, **kwargs) -> None:
        pass


if __name__ == '__main__':
    job = Example()
    job.run()
