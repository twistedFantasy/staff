from django.db import models

from ssm.core.models import BaseModel


class Event(BaseModel):
    title = models.CharField('Title', max_length=256)
    description = models.TextField('Description')
    start_date = models.DateTimeField('Start Date', null=True, blank=True)
    end_date = models.DateTimeField('End Date', null=True, blank=True)
    notify = models.BooleanField('Notify', default=False)
    to = models.CharField('To', max_length=256, null=True, blank=True)
    active = models.BooleanField('Active', default=False)

    class Meta:
        app_label = 'events'
        verbose_name_plural = 'Events'
        ordering = ['title']

# FIXME: tests: return only active for non-staff
