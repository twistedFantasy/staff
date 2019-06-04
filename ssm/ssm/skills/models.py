from django.db import models
from model_utils.choices import Choices

from ssm.users.models import User
from ssm.core.models import BaseModel
from ssm.core.helpers import cleanup


CATEGORY = Choices(
    ('programming_language', 'Programming Language'), ('database', 'Database'),
    ('cloud_technology', 'Cloud Technology'), ('testing_tool', 'Testing Tool'),
    ('frameworks', 'Frameworks'), ('other', 'Other'),
)


class Skill(BaseModel):
    name = models.CharField('Name', max_length=64, unique=True)
    category = models.CharField('Category', max_length=32, null=True, blank=True, default=None, choices=CATEGORY,
        db_index=True)

    def __str__(self):
        return f'{self.name} (skill {self.id})'

    class Meta:
        app_label = 'skills'
        verbose_name_plural = 'Skills'
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.name = cleanup(self.name)
        super().save(*args, **kwargs)


class UserSkillModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    notes = models.TextField('Notes', null=True, blank=True)

    def __str__(self):
        return f'{self.user}-{self.skill}'

    class Meta:
        app_label = 'skills'
        verbose_name_plural = 'UserSkills'
        unique_together = ('user', 'skill')
        ordering = ['skill']


class Verification(BaseModel):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    question = models.TextField('Question')
    answer = models.TextField('Answer')
