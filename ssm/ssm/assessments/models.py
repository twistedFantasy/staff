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
        return f'{self.id} (assessment {self.user})'
