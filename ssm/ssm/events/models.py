from django.db import models

from ssm.core.models import BaseModel


class Event(BaseModel):
    title = models.CharField('Title', max_length=256)
    description = models.TextField('Description')
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    notify = models.BooleanField('Notify', default=False)
    to = models.CharField('To', max_length=256, null=True, blank=True)
    active = models.BooleanField('Active', default=False)

    class Meta:
        app_label = 'events'
        verbose_name_plural = 'Events'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} (event {self.id})'


class FAQ(BaseModel):
    question = models.CharField('Question', max_length=1024)
    answer = models.TextField('Answer', null=True, blank=True)
    order = models.IntegerField('Order', null=True, blank=True)
    active = models.BooleanField('Active', default=False)

    class Meta:
        app_label = 'events'
        verbose_name_plural = 'FAQ'
        ordering = ['order']

    def __str__(self):
        return f'{self.question} (faq {self.id})'
