import csv
import uuid

from django.conf import settings
from celery import Task

from ssm.users.models import User
from ssm.reports.models import History, STATUS
from ssm.core.manage import register


@register()
class WorkingHours(Task):
    abstract = False

    def run(self, history_id, start_date, end_date, *args, **kwargs):
        try:
            history = self.get_history(history_id)
            history.modify(status=STATUS.processing)
            path = f'{settings.MEDIA_ROOT}{uuid.uuid4()}.csv'
            with open(path, mode='w') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for user in User.objects.all():
                    row = [user.full_name, user.email, user.get_working_hours(start_date, end_date)]
                    writer.writerow(row)
            history.modify(path=path, status=STATUS.completed)
        except Exception as e:
            history.modify(msg=str(e), status=STATUS.failed)

    def get_history(self, id):
        return History.objects.get(id=id)


if __name__ == '__main__':
    job = WorkingHours()
    job.run()
