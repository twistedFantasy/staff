from django.db import models

from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel


STATUS = Choices(('new', 'New'), ('active', 'active'), ('closed', 'Closed'), ('failed', 'Failed'))


class Vacancy(BaseModel):
    position = models.CharField('Position', max_length=256)
    description = models.TextField('Description', null=True, blank=True)
    bonus = models.FloatField('Bonus', null=True, blank=True)
    recommended_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.new)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)

    class Meta:
        app_label = 'vacancies'
        verbose_name_plural = 'Vacancies'
        ordering = ['bonus']
