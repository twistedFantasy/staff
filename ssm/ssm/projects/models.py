from django.db import models
from django.contrib import admin
from model_utils.choices import Choices

from ssm.core.models import BaseModel
from ssm.users.models import User

STATUS = Choices(('started', 'Started'), ('in progress', 'In progress'), ('completed', 'Completed'))
ROLES = Choices(('project manager', 'Project manager'), ('developer', 'Developer'), ('tester', 'Tester'),
                ('business analyst', 'Business analyst'), ('front-end developer', 'Front-end developer'),
                ('back-end developer', 'Back-end developer'), ('data scientist', 'Data scientist'),
                ('designer', 'Designer'), ('team lead', 'Team lead'), ('product owner', 'Product owner'))


def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{instance.__class__.__name__}_{instance.id}/{filename}'


class Project(BaseModel):
    name = models.CharField('Name', max_length=32, unique=True)
    description = models.TextField('Description', null=True, blank=True)
    specification = models.FileField('Specification', upload_to=directory_path, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Customer', null=True, blank=True)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.started)
    members = models.ManyToManyField(User, through='MembersModel', related_name='members')
    estimation_in_man_hours = models.IntegerField('Time Estimation In Man-hours', null=True, blank=True)

    def __str__(self):
        return '%s (project %s)' % (self.name, self.id)

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
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

    class Meta:
        app_label = 'projects'
        verbose_name_plural = 'Members'
        unique_together = ('user', 'project', 'role')
        ordering = ['user']
