from datetime import date

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from model_utils.choices import Choices

from ssm.core.models import BaseModel
from ssm.core.helpers import today


BIRTHDAY = 'birthday'
ASSESSMENT = 'assessment'
NOTIFICATIONS = {
    BIRTHDAY: {'subject': settings.BIRTHDAY_SUBJECT, 'text': settings.BIRTHDAY_MESSAGE},
    ASSESSMENT: {'subject': settings.ASSESSMENT_SUBJECT, 'text': settings.ASSESSMENT_MESSAGE},
}
COLOR = Choices(('green', 'Green'), ('yellow', 'Yellow'), ('red', 'Red'), ('black', 'Black'))
LEVEL = Choices(
    ('junior', 'Junior'), ('junior_plus', 'Junior+'), ('middle', 'Middle'), ('middle_plus', 'Middle+'),
    ('senior', 'Senior'), ('senior_plus', 'Senior+'),
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField('Email', unique=True, max_length=256)
    is_active = models.BooleanField('Is Active', default=True)
    is_staff = models.BooleanField('Is Staff', default=False, db_index=True)
    is_superuser = models.BooleanField('Is Superuser', default=False, db_index=True)
    mentor = models.ForeignKey('User', related_name='users_mentor', null=True, blank=True, on_delete=models.SET_NULL)
    level = models.CharField('Level', max_length=32, choices=LEVEL, null=True, blank=True)
    color = models.CharField('Color', max_length=32, choices=COLOR, null=True, blank=True)

    # notifications
    birthday_notification = models.DateField('Birthday Notification', null=True, blank=True)
    assessment_notification = models.DateField('Assessment Notification', null=True, blank=True)

    # metadata
    full_name = models.CharField('Full Name', max_length=256, default='', blank=True)
    ld_number = models.IntegerField('L/D Number', null=True, blank=True)
    position = models.CharField('Position', max_length=68, null=True, blank=True)
    date_of_birth = models.DateField('Date of Birth', null=True, blank=True)
    hired_date = models.DateField('Hired Date', null=True, blank=True)
    end_of_contract = models.DateField('End of Contract', null=True, blank=True)
    education = models.CharField('Education', max_length=32, null=True, blank=True)
    phone_number = models.CharField('Phone Number', max_length=32, null=True, blank=True)
    phone_number2 = models.CharField('Phone Number 2', max_length=32, null=True, blank=True)
    has_card = models.BooleanField('Has Card', default=False)
    has_key = models.BooleanField('Has Key', default=False)
    has_key2 = models.BooleanField('Has Key #2', default=False)
    has_key3 = models.BooleanField('Has Key #3', default=False)
    skype = models.CharField('Skype', max_length=32, null=True, blank=True)
    working_hours = models.IntegerField('Working Hours', default=8)
    skills = models.ManyToManyField('skills.Skill', through='skills.UserSkillModel')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'users'
        verbose_name_plural = 'Users'
        ordering = ['-modified']

    def __str__(self) -> str:
        return f'{self.get_full_name()} (user {self.id})'

    def get_full_name(self) -> str:
        return self.full_name

    def get_short_name(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True

    def get_expected_hours(self) -> int:
        pass  # working_hours * (current_month/period_amount_of_working_days - absences)

    def is_birthday(self) -> bool:
        date_of_birth = self.date_of_birth if self.date_of_birth else None
        birthday_notification = self.birthday_notification if self.birthday_notification else None
        return date_of_birth == today() and birthday_notification != today()

    def is_assessment(self) -> bool:
        from ssm.assessments.models import Assessment
        assessment_notificaiton = self.assessment_notification if self.assessment_notification else None
        return Assessment.objects.filter(user=self, end_date=today()) and assessment_notificaiton != today()

    def notify(self, notification: str) -> None:
        if notification not in NOTIFICATIONS:
            raise Exception('Unknown notification type')
        subject, text = NOTIFICATIONS[notification]['subject'], NOTIFICATIONS[notification]['text']
        send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [self.email])

    def get_working_hours(self, start_date: date, end_date: date) -> int:
        return self.working_hours * 21

    def current_workload(self) -> int:
        from ssm.projects.models import STATUS
        params = {'user': self.id, 'project__status': STATUS.in_progress, 'left_date': None}
        return self.membersmodel_set.filter(**params).aggregate(models.Sum('hours_per_day')).get('hours_per_day__sum', 0)
