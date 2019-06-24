from django.db import models
from model_utils import Choices

from ssm.core.models import BaseModel


STATUS = Choices('pending', 'processing', 'stopped', 'failed', 'completed')
BUSY = [STATUS.pending, STATUS.processing]
DONE = [STATUS.completed]


class Report(BaseModel):
    uid = models.CharField('Unique ID', max_length=64, null=True)
    name = models.CharField('Name', max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'reports'
        verbose_name_plural = 'Reports'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} (report {self.id})'

    def launch(self, start_date, end_date):
        from ssm.reports.configs import REPORTS
        params = {'start_date': start_date, 'end_date': end_date}
        return History.launch(REPORTS[self.uid], params=params, **{'report': self})


class History(BaseModel):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=16, choices=STATUS, default=STATUS.pending, db_index=True)
    path = models.CharField('Path', max_length=256, null=True, blank=True)
    params = models.TextField('Params', null=True)
    msg = models.CharField('msg', max_length=256, null=True, blank=True)
    task_id = models.CharField('task_id', max_length=128, null=True)

    class Meta:
        app_label = 'reports'
        verbose_name_plural = 'Histories'
        ordering = ['-id']

    def __str__(self):
        return f'history_{self.id}'

    @classmethod
    def launch(cls, task, params=None, **kwargs):
        params = params or {}
        history = cls(**kwargs)
        history.save()

        params = {**params, **{'history_id': history.id}}
        task_id = task.delay(**params).task_id
        history.task_id = task_id
        history.save(update_fields=['task_id'])
