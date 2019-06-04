from django.db import models

from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel


STATUS = Choices(('new', 'New'), ('in_progress', 'In progress'), ('completed', 'Completed'), ('failed', 'Failed'))


class Assessment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decision_by = models.ForeignKey(User, related_name='assessments_decision_by', null=True, blank=True,
        on_delete=models.SET_NULL)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.in_progress)
    start_date = models.DateTimeField('Start Date', null=True, blank=True)
    end_date = models.DateTimeField('End Date', null=True, blank=True)
    plan = models.TextField('Plan', null=True, blank=True)
    comments = models.TextField('Comments', null=True, blank=True)
    internal_notes = models.TextField('Internal Notes', null=True, blank=True) # FIXME: test that notes will not be available throuth api by non-staff user
