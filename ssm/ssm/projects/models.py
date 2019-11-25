from django.db import models
from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel
from ssm.core.helpers import cleanup

STATUS = Choices(
    ('waiting', 'waiting'), ('in_progress', 'In progress'), ('completed', 'Completed'), ('failed', 'Failed')
)
ROLES = Choices((
    'project_manager', 'Project manager'), ('developer', 'Developer'), ('tester', 'Tester'),
    ('business_analyst', 'Business Analyst'), ('frontend_developer', 'Front-end Developer'),
    ('backend_developer', 'Back-end Developer'), ('data_scientist', 'Data Scientist'),
    ('designer', 'Designer'), ('team_lead', 'Team Lead'), ('product_owner', 'Product Owner')
)
PRIORITY = Choices(('low', 'Low'), ('normal', 'Normal'), ('high', 'High'))


def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{instance.__class__.__name__}_{instance.id}/{filename}'


class Project(BaseModel):
    name = models.CharField('Name', max_length=32, unique=True)
    link = models.URLField('Link', null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    task_examples = models.TextField('Task Examples', null=True, blank=True)
    technology_stack = models.TextField('Technology Stack', null=True, blank=True)
    specification = models.FileField('Specification', upload_to=directory_path, null=True, blank=True)
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    status = models.CharField('Status', max_length=32, choices=STATUS, default=STATUS.waiting)
    members = models.ManyToManyField(User, through='MembersModel', related_name='members')
    estimation_in_man_hours = models.IntegerField('Estimation In Man-hours', null=True, blank=True)

    class Meta:
        app_label = 'projects'
        verbose_name_plural = 'Projects'
        ordering = ['-modified']

    def __str__(self) -> str:
        return f'{self.name} (project {self.id})'

    def save(self, *args, **kwargs):
        self.name = cleanup(self.name)
        super().save(*args, **kwargs)


class MembersModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    key_person = models.BooleanField('Key Person', default=False)
    role = models.CharField('Role', max_length=64, choices=ROLES, default=ROLES.developer)
    hours_per_day = models.IntegerField('Hours Per Day', default=8)
    joined_date = models.DateField('Joined Date')
    left_date = models.DateField('Left Date',  null=True, blank=True)

    class Meta:
        app_label = 'projects'
        verbose_name_plural = 'Members'
        unique_together = ('user', 'project', 'role')
        ordering = ['user']

    def __str__(self) -> str:
        return f'{self.user}-{self.project}'


class Vacancy(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    level = models.CharField('Level', max_length=128, null=True, blank=True)
    priority = models.CharField('Priority', max_length=32, choices=PRIORITY, default=PRIORITY.normal)
    requirements = models.TextField('Requirements', null=True, blank=True)
    count = models.IntegerField('Count')
    active = models.BooleanField('Active', default=False)

    class Meta:
        app_label = 'projects'
        verbose_name_plural = 'Vacancies'
        ordering = ['project']

    def __str__(self) -> str:
        return f'{self.project}-{self.level}'
