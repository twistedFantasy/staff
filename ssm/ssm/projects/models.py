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


class Project(BaseModel):
    name = models.CharField('Name', max_length=32, unique=True)
    description = models.TextField('Description', null=True, blank=True)
    specification = models.FileField('Specification', null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Customer', null=True, blank=True)
    start_date = models.DateField('Start date', null=True, blank=True)
    end_date = models.DateField('End date', null=True, blank=True)
    status = models.CharField('Status', max_length=32, null=False, blank=False, choices=STATUS, default=STATUS.started)
    members = models.ManyToManyField(User, through='MembershipModel', related_name='members')
    estimation_in_man_hours = models.IntegerField('Time estimation in man-hours', null=True, blank=True)

    def __str__(self):
        return '%s (project %s)' % (self.name, self.id)

    class Meta:
        app_label = 'projects'
        ordering = ['-modified']


class MembershipModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField('Role in project', choices=ROLES, max_length=64, blank=False, null=False,
                            default=ROLES.developer)
    hours_per_day = models.IntegerField('Hours per day', blank=False, null=False, default=8)
    date_joined = models.DateField('Date joined')
    date_left = models.DateField('Date of leaving', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Project members'
        unique_together = ('user', 'project', 'role')
        ordering = ['user']
