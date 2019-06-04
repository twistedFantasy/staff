from django.db import models

from ssm.core.models import BaseModel


class FAQ(BaseModel):
    question = models.CharField('Question', max_length=1024)
    answer = models.TextField('Answer', null=True, blank=True)
    order = models.IntegerField('Order', null=True, blank=True)
    active = models.BooleanField('Active', default=False)

    class Meta:
        app_label = 'faq'
        verbose_name_plural = 'FAQ'
        ordering = ['order']
