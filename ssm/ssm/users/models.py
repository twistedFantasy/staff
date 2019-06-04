from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from model_utils.choices import Choices

from ssm.core.models import BaseModel
from ssm.core.helpers import today, format


BIRTHDAY = 'birthday'
ASSESSMENT = 'assessment'
NOTIFICATIONS = {
    BIRTHDAY: {'subject': settings.BIRTHDAY_SUBJECT, 'text': settings.BIRTHDAY_MESSAGE},
    ASSESSMENT: {'subject': settings.ASSESSMENT_SUBJECT, 'text': settings.ASSESSMENT_MESSAGE},
}
ABSENCE_STATUS = Choices(('new', 'New'), ('veryfing', 'Verifying'), ('approved', 'Approved'), ('rejected', 'Rejected'))
ABSENCE_REASON = Choices(('vacation', 'Vacation'), ('illness', 'Illness'), ('holiday', 'Holiday'), ('other', 'Other'))
ABSENCE_BLOCKED_STATUSES = [ABSENCE_STATUS.approved, ABSENCE_STATUS.rejected]
ABSENCE_RELATED_NAME = 'absences_approved_by'
ASSESSMENT_STATUS = Choices(('new', 'New'), ('in_progress', 'In progress'), ('completed', 'Completed'), ('failed', 'Failed'))


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

    def __str__(self):
        return f'{self.get_full_name()} (user {self.id})'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_birthday(self):
        date_of_birth = format(self.date_of_birth.date()) if self.date_of_birth else None
        birthday_notification = format(self.birthday_notification.date()) if self.birthday_notification else None
        return date_of_birth == format(today()) and birthday_notification != format(today())

    def is_assessment(self):
        from ssm.assessments.models import Assessment
        assessment_notificaiton = format(self.assessment_notification) if self.assessment_notification else None
        return Assessment.objects.filter(user=self, end_date=today()) and \
            assessment_notificaiton != format(today())

    def notify(self, notification):
        if notification not in NOTIFICATIONS:
            raise Exception('Unknown notification type')
        subject, text = NOTIFICATIONS[notification]['subject'], NOTIFICATIONS[notification]['text']
        send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [self.email])


class Absence(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.CharField('Reason', max_length=32, choices=ABSENCE_REASON, default=ABSENCE_REASON.other)
    status = models.CharField('Status', max_length=32, choices=ABSENCE_STATUS, default=ABSENCE_STATUS.new)
    approved_by = models.ForeignKey(User, related_name=ABSENCE_RELATED_NAME, null=True, blank=True,
        on_delete=models.SET_NULL)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End Date')
    notes = models.TextField('Notes', null=True, blank=True)

    def __str__(self):
        return f'{self.id} (absences {self.user.id if self.user else "unknown"})'

    class Meta:
        app_label = 'users'
        verbose_name_plural = 'Absences'
        ordering = ['-id']


class Assessment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decision_by = models.ForeignKey(User, related_name='assessments_decision_by', null=True, blank=True,
        on_delete=models.SET_NULL)
    status = models.CharField('Status', max_length=32, choices=ASSESSMENT_STATUS, default=ASSESSMENT_STATUS.in_progress)
    start_date = models.DateTimeField('Start Date', null=True, blank=True)
    end_date = models.DateTimeField('End Date', null=True, blank=True)
    plan = models.TextField('Plan', null=True, blank=True)
    comments = models.TextField('Comments', null=True, blank=True)
    internal_notes = models.TextField('Internal Notes', null=True, blank=True)

    class Meta:
        app_label = 'users'
        verbose_name_plural = 'Assessments'
        ordering = ['-id']
