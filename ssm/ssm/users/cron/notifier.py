#!/usr/local/bin/python
import django
django.setup()  # noqa @IgnorePep8

from ssm.users.models import User, BIRTHDAY, ASSESSMENT


class Notifier:

    def run(self) -> None:
        users = User.objects.all()
        for user in users:
            if user.is_birthday():
                user.notify(BIRTHDAY)
            if user.is_assessment():
                user.notify(ASSESSMENT)


if __name__ == '__main__':
    job = Notifier()
    job.run()
