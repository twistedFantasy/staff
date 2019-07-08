from django.conf import settings
from django.db import models
from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel
from ssm.core.helpers import cleanup
from ssm.core.google.calendar import Calendar

STATUS = Choices(
    ('waiting', 'waiting'), ('in_progress', 'In progress'), ('completed', 'Completed'), ('failed', 'Failed')
)
ROLES = Choices((
    'project_manager', 'Project manager'), ('developer', 'Developer'), ('tester', 'Tester'),
    ('business_analyst', 'Business Analyst'), ('frontend_developer', 'Front-end Developer'),
    ('backend_developer', 'Back-end Developer'), ('data_scientist', 'Data Scientist'),
    ('designer', 'Designer'), ('team_lead', 'Team Lead'), ('product_owner', 'Product Owner')
)


def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{instance.__class__.__name__}_{instance.id}/{filename}'


class Project(BaseModel):
    name = models.CharField('Name', max_length=32, unique=True)
    description = models.TextField('Description', null=True, blank=True)
    specification = models.FileField('Specification', upload_to=directory_path, null=True, blank=True)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.waiting)
    members = models.ManyToManyField(User, through='MembersModel', related_name='members')
    estimation_in_man_hours = models.IntegerField('Estimation In Man-hours', null=True, blank=True)

    # google services
    google_calendar_id = models.CharField('Google calendar email', max_length=128, null=True, blank=True)

    def __str__(self):
        return f'{self.name} (project {self.id})'

    def save(self, *args, **kwargs):
        self.name = cleanup(self.name)
        if settings.GOOGLE_CALENDAR_SYNC:
            self.google_calendar_id = Calendar.create(self.name)
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'projects'
        verbose_name_plural = 'Projects'
        ordering = ['-modified']


class MembersModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField('Role', max_length=64, choices=ROLES, default=ROLES.developer)
    hours_per_day = models.IntegerField('Hours Per Day', default=8)
    joined_date = models.DateField('Joined Date')
    left_date = models.DateField('Left Date',  null=True, blank=True)

    def save(self, *args, **kwargs):
        if settings.GOOGLE_CALENDAR_SYNC and self.user.id not in self.project.members.values_list('id', flat=True):
            Calendar.add_user(self.user.email, self.project.google_calendar_id)
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'projects'
        verbose_name_plural = 'Members'
        unique_together = ('user', 'project', 'role')
        ordering = ['user']
