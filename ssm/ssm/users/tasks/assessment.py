from datetime import datetime, timedelta

from celery import Task
from django.core import mail
from django.conf import settings

from ssm.users.models import User
from ssm.core.manage import register


@register()
class Assessment(Task):
    abstract = False

    def run(self, *args, **kwargs):
        assessment_date = datetime.now().date() + timedelta(days=settings.ASSESSMENT_NOTIFIER)
        for user in User.objects.filter(is_staff=False, assessment_date=assessment_date):
            mail.send_mail(settings.ASSESSMENT_SUBJECT, settings.ASSESSMENT_TEXT, settings.DEFAULT_FROM_EMAIL, [user.email])


if __name__ == '__main__':
    job = Assessment()
    job.run()
