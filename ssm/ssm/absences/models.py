from django.db import models
from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel
from ssm.calendar.helpers import add_event_to_calendar
from ssm.calendar.calendar_settings import CALENDAR_EMAIL


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
        return f'{self.id} (absences {self.user.id if self.user else "-"})'

    def save(self, *args, **kwargs):
        if self.reason == REASON.holiday and self.user:
            raise ValueError(f"{REASON.holiday} can't be assigned to any user")
        if self.status == STATUS.approved and not self.start_date or not self.end_date:
            raise ValueError(f"Can't change status to {STATUS.approved} with empty start_date and/or end_date")
        if self.status == STATUS.approved:
            summary = '%s\'s absence' % (self.user.full_name)
            description = '%s (%s) is not available due to %s.\n Notes: %s' % (self.user.full_name, self.user.email,
                                                                               self.reason, str(self.notes))
            calendars = self.user.membersmodel_set.values_list('project__google_calendar_email', flat=True)
            for calendar in calendars:
                print(calendar)
                add_event_to_calendar(summary, description, self.start_date, self.end_date, calendar)
            add_event_to_calendar(summary, description, self.start_date, self.end_date, CALENDAR_EMAIL)
        super().save(*args, **kwargs)
