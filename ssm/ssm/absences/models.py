from django.db import models
from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel


STATUS = Choices(('new', 'New'), ('verifying', 'Verifying'), ('approved', 'Approved'), ('rejected', 'Rejected'))
REASON = Choices(('vacation', 'Vacation'), ('illness', 'Illness'), ('holiday', 'Holiday'), ('other', 'Other'))
BLOCKED_STATUSES = [STATUS.approved, STATUS.rejected]
RELATED_NAME = 'absences_approved_by'


class Absence(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.CharField('Reason', max_length=32, choices=REASON, default=REASON.other)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.new)
    decision_by = models.ForeignKey(User, related_name=RELATED_NAME, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    notes = models.TextField('Notes', null=True, blank=True)

    class Meta:
        app_label = 'absences'
        verbose_name_plural = 'Absences'
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.id if self.user else "-"} (absences {self.id})'

    def save(self, *args, **kwargs):
        if self.reason == REASON.holiday and self.user:
            raise ValueError(f"{REASON.holiday} can't be assigned to any user")
        if self.status == STATUS.approved and not self.start_date or not self.end_date:
            raise ValueError(f"Can't change status to {STATUS.approved} with empty start_date and/or end_date")
        super().save(*args, **kwargs)
