from django.db import models
from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel


STATUS = Choices(('new', 'New'), ('veryfing', 'Verifying'), ('approved', 'Approved'), ('rejected', 'Rejected'))
REASON = Choices(('vacation', 'Vacation'), ('illness', 'Illness'), ('holiday', 'Holiday'), ('other', 'Other'))
BLOCKED_STATUSES = [STATUS.approved, STATUS.rejected]
RELATED_NAME = 'absences_approved_by'


class Absence(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.CharField('Reason', max_length=32, choices=REASON, default=REASON.other)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.new)
    approved_by = models.ForeignKey(User, related_name=RELATED_NAME, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End Date')
    notes = models.TextField('Notes', null=True, blank=True)

    def __str__(self):
        return f'{self.id} (absences {self.user.id if self.user else "unknown"})'

    class Meta:
        app_label = 'absences'
        verbose_name_plural = 'Absences'
        ordering = ['-id']
