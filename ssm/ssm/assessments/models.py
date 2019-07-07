from django.db import models
from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel


STATUS = Choices(('new', 'New'), ('in_progress', 'In progress'), ('failed', 'Failed'), ('completed', 'Completed'))


class Assessment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decision_by = models.ForeignKey(User, related_name='assessments_decision_by', null=True, blank=True,
        on_delete=models.SET_NULL)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.in_progress)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    plan = models.TextField('Plan', null=True, blank=True)
    comments = models.TextField('Comments', null=True, blank=True)
    notes = models.TextField('Notes', null=True, blank=True)

    class Meta:
        app_label = 'assessments'
        verbose_name_plural = 'Assessments'
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} (assessment {self.id})'


class Checkpoint(BaseModel):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=256)
    date = models.DateField('Date')

    class Meta:
        app_label = 'assessments'
        verbose_name_plural = 'Checkpoints'
        ordering = ['-id']

    def __str__(self):
        return f'{self.date} (checkpoint {self.id})'


class Task(BaseModel):
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=256)
    description = models.TextField('Description', null=True, blank=True)
    completed = models.BooleanField('Completed', default=False)

    class Meta:
        app_label = 'assessments'
        verbose_name_plural = 'Tasks'
        ordering = ['-id']

    def __str__(self):
        return f'{self.title} (task {self.id})'
